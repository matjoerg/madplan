import json

retter = open("Retter.json", 'r')
varer = open("Varer.json", 'r')
retter_varer = open("RetterVarer.json", 'r')

test1 = json.load(retter)
test2 = json.load(varer)
test3 = json.load(retter_varer)
print(test1)
print(test2)
print(test3)
