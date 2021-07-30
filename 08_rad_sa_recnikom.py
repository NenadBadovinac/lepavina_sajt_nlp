import json

with open('database/recnik.json', 'r') as f:
    recnik = json.load(f)

naslovi = []
for rbr, lista in recnik.items():
    naslovi.append(lista[1])

print(naslovi[15])
