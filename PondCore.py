from abc import ABC, abstractmethod


class PondObject(ABC):
    @abstractmethod
    def as_string(self):
        return ""

    def __str__(self):
        return self.as_string()


class CustomFunction(PondObject):
    def __init__(self, name, effect):
        self.name = name
        self.effect = effect

    def as_string(self):
        return f"{self.name} = {self.effect}"
