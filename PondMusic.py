from PondCore import PondObject


class PondMelody(PondObject):
    def __init__(self, fragments=None):
        self.__fragments = []
        self.__transposition = 0
        if fragments is not None:
            for fragment in fragments:
                self.append_fragment(fragment)

    @property
    def fragments(self):
        return self.__fragments

    def append_fragment(self, fragment):
        self.insert_fragment(len(self.fragments), fragment)

    def insert_fragment(self, index, fragment):
        if isinstance(fragment, (PondMelody, PondNote)):
            self.__fragments.insert(index, fragment)
        elif isinstance(fragment, int):
            self.__fragments.insert(index, PondNote(fragment))
        elif isinstance(fragment, dict):
            self.__fragments.insert(index, PondNote(**fragment))
        else:
            raise ValueError(f"Object {fragment} cannot be "
                             f"interpreted as PondNote or PondMelody")

    def clear_fragments(self):
        self.__fragments = []

    def transpose(self, steps):
        for fragment in self.fragments:
            fragment.transpose(steps)
        self.__transposition += steps

    def render_fragments(self):
        return map(str, self.fragments)

    def ordered_notes(self):
        ordered = []
        for item in self.fragments:
            if isinstance(item, PondNote):
                ordered.append(item)
            else:
                ordered.extend(item.ordered_notes())
        return ordered

    def as_string(self):
        return f"{{{' '.join(self.render_fragments())}}}"

    def __len__(self):
        return len(self.ordered_notes())


class PondFragment(PondMelody):
    def as_string(self):
        return ' '.join(self.render_fragments())


class PondPhrase(PondMelody):
    def as_string(self):
        try:
            return f"{self.fragments[0]} ({' '.join(list(self.render_fragments())[1:])})"
        except IndexError:
            return super().as_string()


class PondTuplet(PondMelody):
    def __init__(self, num=3, den=2, duration=4, notes=None, add_phrasing=False):
        super().__init__(notes)
        self.tuplet_info = f"{num}/{den} {duration}"
        self.add_phrasing = add_phrasing

    def as_string(self):
        return f"\\tuplet {self.tuplet_info} {{{' '.join(self.render_fragments())}}}"


class PondNote(PondObject):
    def __init__(self, pitch, duration="4", articulation="", dynamic="",
                 octave=0, tie=False, expression="", dotted=False, begin_phrase=False,
                 end_phrase=False):
        if isinstance(pitch, PondPitch):
            self.pitch = pitch
        else:
            self.pitch = PondPitch(pitch, octave)
        self.duration = str(duration) + '.' if dotted else str(duration)
        self.articulation = articulation
        self.dynamic = dynamic
        self.tie = "~" if tie else ""
        self.expressions = expression
        self.pre_marks = []
        self.post_marks = []
        self.auxiliary_pitches = {}
        self.phrase_mark = ""
        if begin_phrase:
            self.phrase_data('begin')
        elif end_phrase:
            self.phrase_data('end')

    def phrase_data(self, status="none"):
        if status == "begin":
            self.phrase_mark = " ("
        elif status == "end":
            self.phrase_mark = ")"
        else:
            self.phrase_mark = ""

    def make_tie(self, tie=True):
        self.tie = "~" if tie else ""

    @property
    def absolute_int(self):
        return self.pitch.absolute_int

    def make_rest(self):
        self.pitch.make_rest()

    def make_pitch(self):
        self.pitch.make_pitch()

    def set_ignore_accidental(self, value):
        self.pitch.ignore_accidental = value

    @classmethod
    def create_rest(cls, duration):
        note = PondNote(-1, duration=duration)
        note.make_rest()
        return note

    def transpose(self, steps):
        self.pitch.transpose(steps)
        for pitch in self.auxiliary_pitches.values():
            pitch.transpose(steps)

    def pitch_string(self):
        return self.pitch.as_string()

    def as_string(self):
        return (' '.join(map(str, self.pre_marks)) + self.pitch_string() + self.duration +
                self.articulation + self.tie + self.dynamic + self.expressions +
                ' '.join(map(str, self.post_marks)) + self.phrase_mark)

    def trill_marks(self, begin=True, pitched=None, clear=False, relative=True):
        if clear:
            self.pre_marks = []
            self.post_marks = []
            return
        trill_mark = "\\startTrillSpan " if begin else "\\stopTrillSpan "
        if isinstance(pitched, PondPitch):
            self.pre_marks += ["\\pitchedTrill "]
            self.post_marks += [trill_mark, pitched]
        elif isinstance(pitched, (str, int)):
            octave = self.pitch.octave if relative else 0
            pitched = PondPitch(pitched, octave)
            self.pre_marks += ["\\pitchedTrill "]
            self.auxiliary_pitches["trill"] = pitched
            self.post_marks += [trill_mark, pitched]
        else:
            self.post_marks += [trill_mark]


class PondChord(PondNote):
    def __init__(self, pitches: list, *args):
        super().__init__(pitches[0], *args)
        self.pitches = pitches

    def pitch_string(self):
        return f"<{' '.join(map(str, self.pitches))}>"


class PondNoteGroup(PondObject):
    def __init__(self, duration=4, main_pitches=None, articulation="",
                 dynamic="", tie_data=None, expression=""):
        self.main_pitches = main_pitches or []  # More than one element makes a chord.
        self.__auxiliary_pitches = {}
        self.duration = str(duration)
        self.articulation = articulation
        self.dynamic = dynamic
        self.tie_data = tie_data or [False for _ in range(len(main_pitches))]
        self.expressions = expression
        self.format_string = "{pitch_data}{non_pitch_data}{trill}"

    def all_pitches(self):
        for pitch in self.main_pitches:
            yield pitch
        for pitch in self.__auxiliary_pitches.values():
            yield pitch

    def non_pitch_data(self):
        return self.duration + self.articulation + self.dynamic

    def pitch_data(self):
        if len(self.main_pitches) > 1:
            return str(self.main_pitches[0])
        else:
            return f"<{' '.join(self.string_main_pitches())}>"

    def string_main_pitches(self):
        for idx in range(self.main_pitches):
            pitch = self.main_pitches[idx]
            try:
                tie = "~" if self.tie_data[idx] else ""
            except IndexError:
                tie = ""
            yield str(pitch) + tie

    def transpose(self, steps):
        for pitch in self.all_pitches():
            pitch.transpose(steps)

    def add_trill(self, pitch, octave=0, relative=False):
        if not isinstance(pitch, PondPitch):
            octave = self.main_pitches[0].octave if relative else octave
            pitch = PondPitch(pitch, octave)
        self.__auxiliary_pitches['trill'] = pitch
        self.format_string = ("\\pitchedTrill {pitch_data}{non_pitch_data} "
                              "\\startTrillSpan {trill}")

    def remove_trill(self):
        self.format_string = "{pitch_data}{non_pitch_data}{trill}"
        self.__auxiliary_pitches.pop('trill')

    def end_trill(self):
        self.format_string = "{pitch_data}{non_pitch_data}{trill} \\stopTrillSpan"

    def from_auxiliary(self, key):
        if key in self.__auxiliary_pitches:
            return str(self.__auxiliary_pitches[key])
        else:
            return ""

    def as_string(self):
        string = self.format_string.format(pitch_data=self.pitch_data(),
                                           non_pitch_data=self.non_pitch_data(),
                                           trill=self.from_auxiliary('trill'))
        return string


class PondPitch(PondObject):
    pitch_names = {0: ["bis", "c"],
                   1: ["des", "cis"],
                   2: ["d", "d"],
                   3: ["es", "dis"],
                   4: ["fes", "e"],
                   5: ["f", "eis"],
                   6: ["ges", "fis"],
                   7: ["g", "g"],
                   8: ["aes", "gis"],
                   9: ["a", "a"],
                   10: ["bes", "ais"],
                   11: ["b", "ces"],
                   -1: ["r", "r"]
                   }
    default_key_data = [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0]

    def __init__(self, pitch=0, octave=0, ignore_accidental=False):
        if isinstance(pitch, str):
            pitch = self.__init_from_string(pitch)
        if isinstance(pitch, tuple):
            pitch = pitch[0]
            octave = pitch[1]
        self.__pitch = 0
        self.__octave = octave
        self.pitch = pitch
        self.ignore_accidental = ignore_accidental

    @property
    def pitch(self):
        return self.__pitch

    @pitch.setter
    def pitch(self, value):
        self.__pitch = value
        while self.__pitch > 11:
            self.__pitch -= 12
            self.__octave += 1
        while self.__pitch < 0:
            self.__pitch += 12
            self.__octave -= 1

    @property
    def octave(self):
        return self.__octave

    @property
    def pitch_data(self):
        return self.pitch, self.octave

    @property
    def absolute_int(self):
        return self.pitch + (self.octave * 12)

    def make_rest(self):
        self.__pitch = -1

    def make_pitch(self):
        self.__pitch = 0

    @classmethod
    def __init_from_string(cls, string):
        for pitch, names in cls.pitch_names.items():
            if string in names:
                return pitch
        raise ValueError(f"The note name {string} is currently not supported by PyPond")

    def note_string(self, key_data=None, name_position=None):
        key_data = key_data or self.default_key_data
        name_position = name_position or key_data[self.pitch]
        if self.ignore_accidental:
            return self.pitch_names[self.pitch][name_position][0]
        return self.pitch_names[self.pitch][name_position]

    def octave_string(self):
        if self.pitch == -1:
            return ""
        if self.octave > 0:
            return "'" * self.octave
        return "," * self.octave

    def transpose(self, steps):
        if self.pitch == -1:
            return
        self.pitch += steps

    def as_string(self):
        return self.note_string() + self.octave_string()

    @classmethod
    def from_absolute_int(cls, pitch_value):
        new_pitch = PondPitch()
        new_pitch.transpose(pitch_value)
        return new_pitch
