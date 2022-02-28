from PondCommand import PondAbstractCommand
from PondCore import PondObject


class PondScore(PondAbstractCommand):

    def __init__(self, *subtags):
        super().__init__(*subtags)
        self.__stave = []

    @property
    def tag_name(self):
        return "score"

    def add_staff(self, new_staff):
        if self.__stave:
            try:
                assert isinstance(new_staff, PondStaff)
                assert isinstance(self.__stave[0], PondStaff)
            except AssertionError:
                raise ValueError("To add more than one staff to a PondScore, "
                                 "you must use the PondStaff class")
        self.__stave.append(new_staff)

    def clear_staves(self):
        self.__stave.clear()

    def as_string(self):
        return (f"\\{self.tag_name} {{\n" 
                f"<<{' '.join(map(str, self.__stave))}>>"
                f"}}")


class PondKey(PondAbstractCommand):
    minor = "\\minor"
    major = "\\major"

    def __init__(self, key, *subcommands):
        super().__init__(*subcommands)
        self.key = key

    @property
    def tag_name(self):
        return "key"

    def as_string(self):
        return f"\\{self.tag_name} {{{self.key} {self.subcommands}}}\n"


class PondTimeSignature(PondAbstractCommand):

    def __init__(self, beat_number, beat_value, traditional=True):
        super().__init__()
        if traditional:
            self.validate_beats(beat_value)
        self.time = f"{beat_number}/{beat_value}"

    @property
    def tag_name(self):
        return "time"

    @staticmethod
    def validate_beats(beat):
        power = 1
        while beat != (2 ** power):
            power += 1
            if power > 8:
                raise ValueError(f"Beat value should be a power of 2 and smaller than 258 \n"
                                 f"Current value: {beat}")

    def as_string(self):
        return f"\\{self.tag_name} {self.time}\n"


class PondStaff(PondObject):

    def __init__(self):
        self.__voices = []
        self.__key_signature = ""
        self.__time_signature = ""
        self.__music = ""
        self.top_level_text = []
        self.with_comands = {}  #{"omit": "TimeSignature"}

    @property
    def tag_name(self):
        return "new Staff"

    @property
    def key_signature(self):
        return self.__key_signature

    @key_signature.setter
    def key_signature(self, value):
        if isinstance(value, (PondKey, str)):
            self.__key_signature = str(value)

    @property
    def time_signature(self):
        return self.__time_signature

    @time_signature.setter
    def time_signature(self, value):
        if isinstance(value, (PondTimeSignature, str)):
            self.__key_signature = str(value)

    def add_voice(self, voice):
        self.__voices.append(str(voice))

    def get_voices(self):
        if len(self.__voices) > 1:
            backslash_string = " \\\\ "
            return f"<< {backslash_string.join(self.__voices)} >>"
        else:
            return self.__voices[0]

    def add_with_command(self, key, value):
        self.with_comands[key] = value

    def with_string(self):
        if self.with_comands:
            commands = "\n".join([f"\\{command} {parameter}" for
                                  command, parameter in self.with_comands.items()])
        else:
            return ""
        return f"\\with {{\n{commands}\n}}\n"

    @property
    def top_text(self):
        return '\n'.join(self.top_level_text)

    def as_string(self):
        return (f"\\{self.tag_name} "
                f"{self.with_string()}"
                f"{{\n"
                f"{self.top_text}"
                f"{self.key_signature}"
                f"{self.time_signature}"
                f"{self.get_voices()}\n"
                f"}}")


class PondVoice:
    def __init__(self, relative):
        self.relative = relative
