import requests
from bs4 import BeautifulSoup as BS
import json
import string

def tekst_ekstrakt(url):
    stranica = requests.get(url)
    html = BS(stranica.content, 'html.parser')
    naslov = html.find('h2')
    print(naslov)
    naslov = naslov.text
    sadrzaj = html.find('div', id = 'novost')
    sadrzaj = sadrzaj.text
    sadrzaj = sadrzaj.split()
    sadrzaj = list(map(lambda rec: rec.strip(string.punctuation + string.whitespace), sadrzaj))
    sadrzaj = list(map(lambda rec: rec.lower(), sadrzaj))
    sadrzaj_1 = []
    for rec in sadrzaj:
        if len(rec) < 30:
            sadrzaj_1.append(rec)
    sadrzaj = sadrzaj_1
    #sadrzaj = [rec for rec in sadrzaj if len(rec) < 30]
    return naslov, sadrzaj


    
with open("database/vesti_iz_hriscanskog_sveta_15/vesti.txt", 'r') as f:  
    linkovi_1 = []
    for link in f:
        link = link.rstrip('\n')
        linkovi_1.append(link)
    linkovi = linkovi_1
    
    #linkovi = [link.rstrip('\n') for link in f]
    
#print(linkovi)

base = 'http://www.manastir-lepavina.org/'

for link in linkovi:

    url = base + link
    naslov, sadrzaj = tekst_ekstrakt(url)
    
    recnik = {}
    recnik['naslov'] = naslov
    recnik['sadrzaj'] = sadrzaj

    putanja = 'database/vesti_iz_hriscanskog_sveta_15/' + link[14:] + '.json'
    
    with open(putanja, 'w') as f:
        json.dump(recnik, f)
        
   #with open(putanja, "w") as f:
   #    f.write(str(recnik))

