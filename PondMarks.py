class Dynamics:
    pianissimo = "\\pp"
    piano = "\\p"
    mezzo_piano = "\\mp"
    mezzo_forte = "\\mf"
    forte = "\\f"
    fortissimo = "\\ff"
    forte_piano = "\\fp"
    sforzato = "\\sf"
    sforzatissimo = "\\sff"
    subito_piano = "\\sp"
    subitpo_pianissimo = "\\ssp"
    sforzando = "\\sfz"
    riforzando = "\\rfz"
    crescendo_hairpin = "\\<"
    diminuendo_hairpin = "\\>"

    @classmethod
    def custom_dynamic(cls, identifier, number):
        assert identifier in ("p", "f")
        assert 0 <= number < 6
        if number == 0:
            return f"\\m{identifier}"
        else:
            return f"\\{identifier * number}"


class MiscMarks:
    relative = "\\relative"
    repeat = "\\repeat"
    end_tag = "\\!"


class Articulations:
    marcato = "-^"
    stopped = "-+"
    tenuto = "--"
    staccatissimo = "-!"
    accent = "->"
    staccato = "-."
    portato = "-_"
    espressivo = "\\espressivo"
    mordent = "\\mordent"
    trill = "\\trill"
    short_fermata = "\\shortfermata"
    fermata = "\\fermata"
    long_fermata = "\\longfermata"
    glissando = "\\gliss"
