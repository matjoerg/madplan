from madplan.objects.vare import Vare
from madplan.model import model


class Ret:
    """ """

    def __init__(self, navn):
        self.navn = navn
        self.ugedag = None
        self.varer = []
        self.initialize()

    def initialize(self):
        db = model.get_db()
        cur = db.cursor()
        cur.execute("""SELECT Varer.navn, RetterVarer.antal, Kategorier.navn kategori FROM Retter 
                    INNER JOIN Kategorier ON Varer.kategori_id = Kategorier.id
                    INNER JOIN RetterVarer ON Retter.id = RetterVarer.ret_id 
                    INNER JOIN Varer on RetterVarer.vare_id = Varer.id 
                    WHERE Retter.navn = '{}';""".format(self.navn))
        varer = cur.fetchall()
        for vare in varer:
            self.tilfoj_vare(vare['navn'], vare['antal'], vare['kategori'])

    def tilfoj_vare(self, navn, antal=1, kategori=None):
        found_duplicate = False
        for index, other_vare in enumerate(self.varer):
            if other_vare.navn == navn:
                self.varer[index].antal += antal
                found_duplicate = True
                break

        if not found_duplicate:
            vare = Vare(navn, antal, kategori)
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
