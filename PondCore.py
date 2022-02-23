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


class DurationInterface:
    simple_converter = {0.125: "32",
                        0.25: "16",
                        0.5: "8",
                        1: "4",
                        2: "2",
                        4: "1",
                        }
    dotted_converter = {0.125: "32",
                        0.25: "16",
                        0.375: "16.",
                        0.5: "8",
                        0.75: "8.",
                        1: "4",
                        1.5: "4.",
                        2: "2",
                        3: "2.",
                        4: "1",
                        6: "1."
                        }

    reverse_dotted_converter = {value: key for key, value in dotted_converter.items()}

    @classmethod
    def get_duration_list(cls, duration, simple=False, start=0, max_duration=6):
        if duration % 0.125:
            raise ValueError(f"DurationConverter currently only accepts "
                             f"values up to the semiquaver. Attempted value: {duration}")
        duration_list = []
        current_value = duration - start
        next_value = 0
        converter = cls.simple_converter if simple else cls.dotted_converter
        if start:
            duration_list.append(cls.dotted_converter[start])
        while current_value > 0:
            if current_value > max_duration:
                diff = current_value - max_duration
                current_value -= max_duration
                next_value += diff
            if current_value in converter:
                duration_list.append(converter[current_value])
                current_value = next_value
                next_value = 0
            else:
                current_value -= 0.125
                next_value += 0.125
        return duration_list

    @classmethod
    def get_fragment_duration(cls, fragment):
        """
        Warning: does not provide correct duration of tuplets
        """
        mapped = map(lambda x: cls.get_real_duration(x.duration), fragment.ordered_notes())
        return sum(mapped)

    @classmethod
    def get_remainig_tuplet_time(cls, tuplet):
        target, base_value, duration = tuplet.data
        pond_duration = int(base_value) * int(duration)
        base_duration = cls.get_real_duration(pond_duration)
        total_duration = cls.get_fragment_duration(tuplet)
        remaining_beats = target - ((total_duration / base_duration) % target)
        if remaining_beats == target:
            remaining_beats = 0
        return int(remaining_beats), base_duration

    @classmethod
    def get_pond_duration(cls, duration):
        try:
            return cls.dotted_converter[float(duration)]
        except KeyError:
            raise ValueError(f"DurationConverter currently only accepts "
                             f"values up to the semiquaver. Attempted value: {duration}")

    @classmethod
    def get_real_duration(cls, duration):
        try:
            return cls.reverse_dotted_converter[str(duration)]
        except KeyError:
            raise ValueError(f"DurationConverter requires a valid Lilypond duration. "
                             f"Attempted value: {duration}")

    @classmethod
    def is_complete_tuplet(cls, tuplet):
        remaining, base = cls.get_remainig_tuplet_time(tuplet)
        if remaining != 0:
            return False
        return True