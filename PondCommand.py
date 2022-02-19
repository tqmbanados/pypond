from abc import abstractmethod, ABC
from PondCore import PondObject


class PondAbstractCommand(PondObject, ABC):
    def __init__(self, *subcommands):
        self.subcommands = " ".join(map(str, subcommands))

    @property
    @abstractmethod
    def tag_name(self):
        return str()

    @abstractmethod
    def as_string(self):
        return f"\\{self.tag_name} {{{self.subcommands}}}"

    def __str__(self):
        return self.as_string()


class PondHeader(PondAbstractCommand):
    @property
    def tag_name(self):
        return "header"

    def as_string(self):
        return f"\\{self.tag_name} {{ tagline = ##f }}"


class PondLayout(PondAbstractCommand):
    @property
    def tag_name(self):
        return "layout"

    def as_string(self):
        return f"\\{self.tag_name} {{}}"


class PondMarkup(PondAbstractCommand):
    italic = "\\italic"
    bold = "\\bold"
    small = "\\smaller"

    def __init__(self, text, *subcommands):
        super().__init__(*subcommands)
        self.text = text

    @property
    def tag_name(self):
        return "markup"

    def as_string(self):
        return f"\\{self.tag_name} {{{self.subcommands} {self.text}}}"

    def add_to_note(self, over=True):
        position_marker = "^" if over else "-"
        return position_marker + str(self)


class PondPaper(PondAbstractCommand):

    def __init__(self, *subcommands):
        super().__init__(self, *subcommands)
        self.__margins = {"top-margin": 0,
                          "bottom-margin": 0,
                          "left-margin": 0,
                          "right-margin": 0}

    def get_margins(self):
        margin_strings = []
        for margin, value in self.__margins.items():
            if value:
                margin_strings.append(f"{margin} = {value}")
        return "  " + "\n".join(margin_strings)

    def set_margin(self, margin, value):
        if value < 0:
            return
        self.__margins[margin] = value

    @property
    def tag_name(self):
        return "paper"

    def as_string(self):
        return f"\\{self.tag_name} {{{self.get_margins()}}}"
