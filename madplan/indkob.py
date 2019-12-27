class Indkobsliste:
    """ """

    def __init__(self):
        self.alle_ingredienser = []

    def saml_alle_ingredienser(self, ugeplan):
        for ret in ugeplan.retter:
            for ingrediens in ret.ingredienser:
                found_duplicate = False
                for index, other_ingrediens in enumerate(self.alle_ingredienser):
                    if ingrediens == other_ingrediens:
                        found_duplicate = True
                        self.alle_ingredienser[index].antal += ingrediens.antal

                if not found_duplicate:
                    self.alle_ingredienser.append(ingrediens)

        return self.alle_ingredienser

    def __str__(self):
        
