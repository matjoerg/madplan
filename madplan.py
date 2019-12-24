import sys
import string
import numpy as np
from flask import Flask

app = Flask(__name__)

kategorier = ["Frugt og grønt", "Mejeri", "Kolonial", "Kød"]

alle_hovedretter = {"1 - Kartoffelsalat med frikadeller": {kategorier[0]: ["Kartofler", "Rødløg", "Løg", "Æbler", "Purløg"], 
                                                           kategorier[1]: ["Creme fraiche", "Mælk", "Æg"], 
                                                           kategorier[2]: ["Hvedemel"]},
                    "2 - Æggekage": {kategorier[0]: ["Purløg", "Kartofler", "Løg"],
                                     kategorier[1]: ["Æg"],
                                     kategorier[2]: ["Rugbrød"],
                                     kategorier[3]: ["Spegepølse"]},
                    "3 - Risotto med rodfrugter": {kategorier[0]: ["Rodfrugter", "Pærer", "Løg"],
                                                   kategorier[1]: ["Parmesanost"],
                                                   kategorier[2]: ["Grødris"]},
                    "4 - Frisk pasta med skinke": {kategorier[0]: ["Champignon"],
                                                   kategorier[1]: ["Fløde", "Revet ost"],
                                                   kategorier[2]: ["Frisk pasta"],
                                                   kategorier[3]: ["Tørret skinke"]},
                    "5 - Lasagne": {kategorier[0]: ["Aubergine", "Gulerødder"],
                                    kategorier[1]: ["Mælk", "Revet ost", "Smør"],
                                    kategorier[2]: ["Lasagneplader", "Hvedemel", "Hakkede tomater"],
                                    kategorier[3]: ["Oksefars"]},
                    "6 - Ristaffel": {kategorier[0]: ["Rød peber", "Bananer", "Forårsløg", "Æbler", "Ærter", "Majs"],
                                      kategorier[2]: ["Rosiner", "Peanuts", "Kokosmel", "Ris", "Kokosmælk"],
                                      kategorier[3]: ["Kylling"]},
                    "7 - Friske forårsruller": {kategorier[0]: ["Mango", "Rød peber", "Gulerødder", "Agurk", "Forårsløg"],
                                                kategorier[2]: ["Sursød sauce", "Rispapir", "Risnudler"],
                                                kategorier[3]: ["Kylling"]},
                    "8 - Pasta/kødsovs": {kategorier[0]: ["Squash", "Champignon", "Løg"],
                                          kategorier[1]: ["Mælk", "Revet ost"],
                                          kategorier[2]: ["Spaghetti", "Hakkede tomater"],
                                          kategorier[3]: ["Oksefars"]},
                    "9 - Pitabrød": {kategorier[0]: ["Majs", "Ærter", "Rød peber", "Avocado", "Agurk"],
                                     kategorier[1]: ["Æg", "Tun", "Pitabrød", "Dressing"]},
                    "10 - Wok": {kategorier[0]: ["Wokblanding"],
                                 kategorier[2]: ["Kokosmælk", "Ris", "Hakkede tomater"],
                                 kategorier[3]: ["Kylling"]},
                    "11 - Mexicanske panderkager": {kategorier[0]: ["Majs", "Ærter", "Agurk", "Rød peber", "Avocado", "Løg"],
                                                    kategorier[1]: ["Revet ost", "Creme fraiche"],
                                                    kategorier[2]: ["Taco sauce", "Tortillas", "Kidneybønner"],
                                                    kategorier[3]: ["Oksefars"]},
                    "12 - Chili con carne": {kategorier[0]: ["Squash", "Løg", "Avocado", "Creme fraiche"],
                                             kategorier[2]: ["Hakkede tomater", "Kidneybønner", "Sorte bønner", "Mørk chokolade"],
                                             kategorier[3]: ["Oksefars"]},
                    "13 - Svinemørbrad i flødesovs": {kategorier[0]: ["Kartofler", "Champignon", "Rød peber", "Løg"],
                                                      kategorier[1]: ["Fløde"],
                                                      kategorier[3]: ["Svinemørbrad"]},
                    "14 - Grøntsagssuppe": {kategorier[0]: ["Kartofler", "Porrer", "Løg", "Gulerødder"],
                                            kategorier[1]: ["Fløde"],
                                            kategorier[2]: ["Græskarkerner", "Flutes"],
                                            kategorier[3]: ["Chorizo"]},
                    "15 - Kylling i fad": {kategorier[0]: ["Porrer", "Gulerødder", "Rød peber", "Løg", "Hvidløg", "Kartofler"],
                                           kategorier[1]: ["Fløde", "Pikantost"],
                                           kategorier[2]: ["Hakkede tomater", "Tomatpuré"],
                                           kategorier[3]: ["Kylling"]},
                    "16 - Fiskefrikadeller og rugbrød": {kategorier[1]: ["Smør"],
                                                         kategorier[2]: ["Rugbrød", "Citron", "Remoulade"],
                                                         kategorier[3]: ["Fiskefars"]},
                    "17 - Grillkød med rodfrugter": {kategorier[0]: ["Rodfrugter", "Majskolber", "Aubergine", "Rød peber"],
                                                     kategorier[3]: ["Grillkød"]},
                    "18 - Fisk i fad": {kategorier[0]: ["Porrer", "Gulerødder", "Rød peber", "Løg", "Hvidløg", "Kartofler"],
                                        kategorier[1]: ["Pikantost"],
                                        kategorier[3]: ["Fisk"]},
                    "19 - Burger": {kategorier[0]: ["Agurk", "Rød peber", "Grøn salat", "Løg", "Avocado"],
                                    kategorier[1]: ["Mozarella", "Burgerboller", "Dressing", "Ketchup"],
                                    kategorier[3]: ["Oksefars"]},
                    "20 - Grillkød med bagekartofler": {kategorier[0]: ["Aubergine", "Rød peber", "Bagekartofler"],
                                                        kategorier[1]: ["Creme fraiche"],
                                                        kategorier[3]: ["Grillkød"]},
                    "21 - Fars på porrebund": {kategorier[0]: ["Porrer", "Kartofler", "Løg"],
                                               kategorier[2]: ["Rasp"],
                                               kategorier[3]: ["Kalvefars"]},
                    "22 - Squashtærte": {kategorier[0]: ["Squash", "Porrer"],
                                         kategorier[1]: ["Mælk", "Hytteost", "Feta"],
                                         kategorier[2]: ["Tærtedej"],
                                         kategorier[3]: ["Tørret skinke"]}}


alle_salater = {"a - Broccolisalat": {kategorier[0]: ["Broccoli", "Tranebær"],
                                      kategorier[1]: ["Hytteost"],
                                      kategorier[2]: ["Solsikkekerner"]},
                "b - Spidskål med æble": {kategorier[0]: ["Æbler", "Spidskål"],
                                          kategorier[2]: ["Mandler"]},
                "c - Grøn salat": {kategorier[0]: ["Agurk", "Rød peber", "Grøn salat", "Avocado"],
                                   kategorier[1]: ["Feta"]},
                "d - Serrano salat": {kategorier[0]: ["Granatæble", "Grøn salat", "Avocado"],
                                      kategorier[1]: ["Mozarella"],
                                      kategorier[3]: ["Tørret skinke"]}}

alle_retter = {**alle_hovedretter, **alle_salater}

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

@app.route("/")
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
