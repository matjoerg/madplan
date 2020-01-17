import sys
import string
import numpy as np
from madplan.old_db import Database
from madplan.objects.ingrediens import Ingrediens
from madplan.objects.ret import Ret
from madplan.objects.indkob import Indkobsliste

db = Database()

kategorier = ["Frugt og grønt", "Mejeri", "Kolonial", "Kød"]
alle_retter = db.get_db()

def print_alle_retter(detaljeret):
    s = "-----Hovedretter-----" + "\n"
    for ret in alle_retter.keys():
        varer = alle_retter[ret]
        if ret[0] == 'a':
            s += '\n' + '-----Salater-----' + '\n'
        s += '\n' + '*** ' + ret + ' ***' + '\n'
        if detaljeret:
            for kategori in list(varer.keys()):
                s += '\n' + '__' + kategori + '__' + '\n'
                for vare in varer[kategori]:
                    s += vare + '\n'
    return s

def print_indkobsliste(numre):
    s = "Madplan" + "\n\n"
    alle_varer = [[] for _ in range(len(kategorier))]
    for ret in alle_retter.keys():
        if ret.split('-')[0][:-1] in numre:
            varer = alle_retter[ret]
            for kategori in list(varer.keys()):
                kategori_nummer = kategorier.index(kategori)
                for vare in varer[kategori]:
                    if vare not in alle_varer[kategori_nummer]:
                        alle_varer[kategori_nummer].append(vare)

    madplan_numre = np.array([ret.split('-')[0][:-1] for ret in alle_retter.keys()])
    for nummer in numre:
        ret = list(alle_retter.keys())[np.where(nummer==madplan_numre)[0][0]]
        s += '*** ' + ret + ' ***' + '\n'

    s += "\n" + "Indkøbsliste" + "\n"
    for kategori_nummer, varer in enumerate(alle_varer):
        s += '\n' + '__' + kategorier[kategori_nummer] + '__' + '\n'
        for vare in varer:
            s += vare + '\n'

    return s

def print_madplan():
    detaljeret = False
    numre = []
    for input in sys.argv[1:]:
        if len(input) < 3:
            numre.append(input)
        elif input == 'lang':
            detaljeret = True
        else:
            print("Input must be integers or letters.")

    if len(numre) == 0:
        return print_alle_retter(detaljeret)
    else:
        return print_indkobsliste(numre)

if __name__ == "__main__":
    s = print_madplan()
    print(s)
