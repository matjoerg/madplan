from madplan.objects.ret import Ret


class Ugeplan:
    """ """

    def __init__(self):
        self.retter = []

    def tilfoj_ret(self, ret_navn, ugedag=None):
        ret = Ret(ret_navn)
        ret.ugedag = ugedag
        self.retter.append(ret)

    def __str__(self):
        s = '*** Madplan ***\n'
        s += '\n'
        for ret in self.retter:
            s += '*** {}: {} ***\n'.format(ret.ugedag, ret.navn)
            for vare in ret.varer:
                s += '{} ({}) ({})\n'.format(vare.navn, vare.antal, vare.kategori)
            s += '\n'
        return s
