from abc import ABC, abstractmethod


class PondObject(ABC):
    @abstractmethod
    def as_string(self):
        return ""

    def __str__(self):
        return self.as_string()