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
        self.__header = value.as_string()

    @property
    def paper(self):
        return self.__paper

    @paper.setter
    def paper(self, value):
        self.__paper = value.as_string()

    @property
    def layout(self):
        return self.__layout

    @layout.setter
    def layout(self, value):
        self.__layout = value.as_string()

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, value):
        self.__score = value.as_string()

    @property
    def functions(self):
        return "\n".join(self.__functions)

    def add_function(self, value):
        self.__functions.append(value)

    def create_file(self):
        return "\n".join([self.header, self.paper, self.functions,
                          self.score, self.layout])


class PondRender:
    def __init__(self, **config):
        self.__file_name = "temp_pypond.ly"
        self.__folder_path = os.path.join("ly_files")
        self.__auto_write = False
        self.__version = '\\version "2.22.1"'
        self.__format = "png"
        self.current_file = self.__version + "\n"
        self.set_config(**config)

    @property
    def __file_path(self):
        return os.path.join(self.__folder_path, self.__file_name)

    @property
    def __render_options(self):
        return (f"-o{self.__folder_path} "
                f"-dbackend=eps -dno-gs-load-fonts -dinclude-eps-fonts "
                f"--png {self.__file_path}")

    def set_config(self, **config):
        for name, value in config.items():
            attr_name = f"_LyRender__{name}"
            setattr(self, attr_name, value)

    def update(self, new_file):
        if isinstance(new_file, PondDoc):
            new_file = new_file.create_file()
        self.current_file = self.__version + "\n" + new_file
        if self.__auto_write:
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
