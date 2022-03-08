from abc import abstractmethod, ABC
from .PondCore import PondObject


class PondAbstractCommand(PondObject, ABC):
    def __init__(self, *subcommands, **kwcommands):
        self.__subcommands = subcommands
        self.__kwcommands = kwcommands

    @property
    def subcommands(self):
        return " ".join(map(str, self.__subcommands))

    @property
    def kwcommands(self):
        return "\n".join(f"{key} = {value}"
                         for key, value in self.__kwcommands.items())

    @property
    @abstractmethod
    def tag_name(self):
        return str()

    @abstractmethod
    def as_string(self):
        return (f"\\{self.tag_name} {{\n"
                f"{self.subcommands}\n"
                f"{self.kwcommands}}}\n")

    def __str__(self):
        return self.as_string()


class PondHeader(PondAbstractCommand):

    def __init__(self, *subcommands, tagline="##f", **kwcommands):
        super().__init__(*subcommands, tagline=tagline, **kwcommands)

    @property
    def tag_name(self):
        return "header"

    def as_string(self):
        return super().as_string()


class PondLayout(PondAbstractCommand):
    @property
    def tag_name(self):
        return "layout"

    def as_string(self):
        return super().as_string()


class PondMarkup(PondAbstractCommand):
    italic = "\\italic"
    bold = "\\bold"
    small = "\\smaller"

    def __init__(self, text, *subcommands, **kwcommands):
        super().__init__(*subcommands, **kwcommands)
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

    def __init__(self, *subcommands, **kwcommands):
        super().__init__(self, *subcommands, **kwcommands)
        self.__margins = {"top-margin": 0,
                          "bottom-margin": 0,
                          "left-margin": 0,
                          "right-margin": 0}
        self.additional_data = []

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

    def update_margins(self, values):
        self.__margins.update(values)

    @property
    def tag_name(self):
        return "paper"

    def as_string(self):
        return (f"\\{self.tag_name} {{\n"
                f"{self.get_margins()}\n"
                f"{' '.join(self.additional_data)}\n"
                f"}}")


if __name__ == "__main__":
    header = PondHeader(title="miau", composer="Thyme", tagline="##f")
    print(header.as_string())
