# Pregled naslova nepozeljnih tekstova

import json
   
with open('database\\nepozeljni.json', 'r') as f:
    recnik = json.load(f)

naslovi = []
for naslov, sadrzaj in recnik.items():
    naslovi.append(naslov)

for naslov in naslovi:
    print('-', naslov)
