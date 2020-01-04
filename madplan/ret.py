from ingrediens import Ingrediens

class Ret:
    """ """

    def __init__(self, navn):
        self.navn = navn
        self.ingredienser = []

    def tilfoj_ingrediens(self, ingrediens_navn, antal=1, kategori=None):
        found_duplicate = False
        for index, ingrediens in enumerate(self.ingredienser):
            if ingrediens.navn == ingrediens_navn:
                self.ingredienser[index].antal += antal
                found_duplicate = True
                break

        if not found_duplicate:
            ingrediens = Ingrediens(ingrediens_navn, antal, kategori)
            self.ingredienser.append(ingrediens)

    def fjern_ingrediens(self, ingrediens_navn, antal=1):
        for index, ingrediens in enumerate(self.ingredienser):
            if ingrediens.navn == ingrediens_navn:
                self.ingredienser[index].antal -= antal
                if self.ingredienser[index].antal <= 0:
                    del self.ingredienser[index]
                break
        
    def __str__(self):
        return self.navn
