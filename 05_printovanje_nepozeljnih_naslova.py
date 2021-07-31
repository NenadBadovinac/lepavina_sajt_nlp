# Pregled naslova nepozeljnih tekstova

import json
   
with open('database\\nepozeljni.json', 'r') as f:
    recnik = json.load(f)

naslovi = []
for naslov, sadrzaj in recnik.items():
    naslovi.append(naslov)

print('Broj nepozeljnih tekstova:', len(naslovi))

for naslov in naslovi:
    print('-', naslov)

