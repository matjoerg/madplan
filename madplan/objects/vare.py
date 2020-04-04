class Vare:
    """ """

    def __init__(self, navn, kategori=None, antal=1):
        self.navn = navn
        self.antal = antal
        self.kategori = kategori

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.navn == other.navn
        else:
            return False
