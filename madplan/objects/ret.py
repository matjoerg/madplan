from madplan.objects.vare import Vare

class Ret:
    """ """

    def __init__(self, navn):
        self.navn = navn
        self.varer = []

    def tilfoj_vare(self, vare_navn, antal=1, kategori=None):
        found_duplicate = False
        for index, vare in enumerate(self.varer):
            if vare.navn == vare_navn:
                self.varer[index].antal += antal
                found_duplicate = True
                break

        if not found_duplicate:
            vare = Vare(vare_navn, antal, kategori)
            self.varer.append(vare)

    def fjern_vare(self, vare_navn, antal=1):
        for index, vare in enumerate(self.varer):
            if vare.navn == vare_navn:
                self.varer[index].antal -= antal
                if self.varer[index].antal <= 0:
                    del self.varer[index]
                break
        
    def __str__(self):
        return self.navn
