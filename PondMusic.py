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
        if isinstance(fragment, (PondMelody, PondNote)):
            self.__fragments.append(fragment)
        elif isinstance(fragment, int):
            self.__fragments.append(PondNote(fragment))
        elif isinstance(fragment, dict):
            self.__fragments.append(PondNote(**fragment))
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

    def as_string(self):
        return f"{{{' '.join(self.render_fragments())}}}"


class PondFragment(PondMelody):
    def as_string(self):
        return ' '.join(self.render_fragments())


class PondPhrase(PondMelody):
    def as_string(self):
        return f"{self.fragments[0]} ({' '.join(self.render_fragments())})"


class PondTuplet(PondMelody):
    def __init__(self, num=3, den=2, duration=4, notes=None):
        super().__init__(notes)
        self.tuplet_info = f"{num}/{den} {duration}"

    def as_string(self):
        return f"\\tuplet {self.tuplet_info} {{{' '.join(self.render_fragments())}}}"


class PondNote(PondObject):
    def __init__(self, pitch, duration="4", articulation="", score_marks="",
                 octave=4, tie=""):
        self.pitch = PondPitch(pitch, octave)
        self.duration = str(duration)
        self.articulation = "-" + articulation if articulation else ""
        self.score_marks = score_marks
        self.tie = "~" if tie else ""

    def transpose(self, steps):
        self.pitch.transpose(steps)

    def pitch_data(self):
        return self.pitch.as_string()

    def as_string(self):
        return (self.pitch_data() + self.duration +
                self.articulation + self.tie + self.score_marks)


class PondChord(PondNote):
    def __init__(self, pitches: list, *args):
        super().__init__(pitches[0], *args)
        self.pitches = pitches

    def pitch_data(self):
        return f"<{' '.join(map(str, self.pitches))}>"


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

    def __init__(self, pitch, octave=4):
        if isinstance(pitch, str):
            pitch = self.from_string(pitch)
        self.__pitch = pitch
        self.__octave = octave

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

    def make_rest(self):
        self.__pitch = -1

    def make_pitch(self):
        self.__pitch = 0

    def from_string(self, string):
        for pitch, names in self.pitch_names.items():
            if string in names:
                return pitch
        raise ValueError(f"The note name {string} is currently not supported by PyPond")

    def note_string(self, key_data=None, name_position=None):
        key_data = key_data or self.default_key_data
        name_position = name_position or key_data[self.pitch]
        return self.pitch_names[self.pitch][name_position]

    def octave_string(self):
        if self.pitch == -1:
            return ""
        distance = self.__octave - 4
        if distance > 0:
            return "'" * distance
        return "," * distance

    def transpose(self, steps):
        if self.pitch == -1:
            return
        self.pitch += steps

    def as_string(self):
        return self.note_string() + self.octave_string()


