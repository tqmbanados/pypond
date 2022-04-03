import os


class PondDoc:
    def __init__(self):
        self.__header = str()
        self.__paper = str()
        self.__layout = str()
        self.__score = str()
        self.__functions = []

    @property
    def header(self):
        return self.__header

    @header.setter
    def header(self, value):
        self.__header = str(value)

    @property
    def paper(self):
        return self.__paper

    @paper.setter
    def paper(self, value):
        self.__paper = str(value)

    @property
    def layout(self):
        return self.__layout

    @layout.setter
    def layout(self, value):
        self.__layout = str(value)

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, value):
        self.__score = str(value)

    @property
    def functions(self):
        return "\n".join(self.__functions)

    def add_function(self, name, value):
        self.__functions.append(f"{name} = {value}")

    def create_file(self):
        return "\n".join([self.header, self.paper, self.functions,
                          self.score, self.layout])


class PondRender:
    def __init__(self, **config):
        self._file_name = "temp_pypond.ly"
        self._folder_path = os.path.join("ly_files")
        self._auto_write = False
        self._version = '\\version "2.22.1"'
        self._format = "png"
        self._resolution = 200
        self.current_file = self._version + "\n"
        self.set_config(**config)

    @property
    def __file_path(self):
        return os.path.join(self._folder_path, self._file_name)

    @property
    def __render_options(self):
        return (f"-o{self._folder_path} "
                f"-f{self._format} -dbackend=eps -dresolution={self._resolution} "
                f"-dno-gs-load-fonts -dinclude-eps-fonts "
                f""
                f"{self.__file_path}")

    def set_config(self, **config):
        for name, value in config.items():
            attr_name = f"_{name}"
            setattr(self, attr_name, value)

    def update(self, new_file):
        if isinstance(new_file, PondDoc):
            new_file = new_file.create_file()
        self.current_file = self._version + "\n" + new_file
        if self._auto_write:
            self.write()

    def write(self):
        with open(self.__file_path, 'wt') as file:
            file.write(self.current_file)

    def render(self):
        os.system(f"lilypond {self.__render_options} {self.__file_path}")


if __name__ == "__main__":
    render = PondRender(auto_write=True)
    render.update("""
\\header {
    tagline = ##f
    }
\\score {
    {a4 b c d}
    }
    """)
    render.write()
    render.render()
