class Indkobsliste:
    """ """

    def __init__(self):
        self.alle_varer = []

    def saml_alle_varer(self, ugeplan):
        for ret in ugeplan.retter:
            for vare in ret.varer:
                found_duplicate = False
                for index, other_vare in enumerate(self.alle_varer):
                    if vare == other_vare:
                        found_duplicate = True
                        self.alle_varer[index].antal += vare.antal

                if not found_duplicate:
                    self.alle_varer.append(vare)

        return self.alle_varer

#    def __str__(self):
