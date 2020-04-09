from madplan.objects.ret import Ret


class Ugeplan:
    """ """

    def __init__(self):
        self.retter = []
        self.indkobsliste = {}

    def tilfoj_ret(self, ret_navn, ugedag=None):
        ret = Ret(ret_navn)
        ret.ugedag = ugedag
        self.retter.append(ret)

    def lav_indkobsliste(self):
        for ret in self.retter:
            for vare in ret.varer:
                kategori = vare.kategori
                if kategori not in self.indkobsliste.keys():
                    self.indkobsliste[kategori] = [vare]
                else:
                    found_duplicate = False
                    for index, other_vare in enumerate(self.indkobsliste[kategori]):
                        if vare == other_vare:
                            found_duplicate = True
                            self.indkobsliste[kategori][index].antal += vare.antal

                    if not found_duplicate:
                        self.indkobsliste[kategori].append(vare)

        return self.indkobsliste

    def __str__(self):
        s = '*** Madplan ***\n'
        s += '\n'
        for ret in self.retter:
            s += '*** {}: {} ***\n'.format(ret.ugedag, ret.navn)
            for vare in ret.varer:
                s += '{} ({}) ({})\n'.format(vare.navn, vare.antal, vare.kategori)
            s += '\n'
        return s
