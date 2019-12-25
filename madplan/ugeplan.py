class Ugeplan:
    """ """

    def __init__(self, ugenummer=None):
        self.ugenummer = ugenummer
        self.retter = []
       
    def tilfoj_ret(self, ret, ugedag=None):
        ret.ugedag = ugedag
        self.retter.append(ret)

    def __str__(self):
        s = '*** Madplan ***\n'
        s += '\n'
        for ret in self.retter:
            s += '{}: {}\n'.format(ret.ugedag, ret.navn)
        return s
