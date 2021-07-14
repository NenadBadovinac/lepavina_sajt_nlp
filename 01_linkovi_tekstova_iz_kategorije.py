import requests
from bs4 import BeautifulSoup as BS

def eksport_linkova(url):
    stranica = requests.get(url)
    html = BS(stranica.content, 'html.parser')
    linkovi = []
    paragrafi = html.find_all('p', 'naslov')
    for paragraf in paragrafi:
        link = paragraf.find('a')
        link = link['href']
        linkovi.append(link)
    return linkovi

stranice = list(range(100))
baza = 'http://manastir-lepavina.org/kategorija.php?id=15&page='
    
linkovi = []
    
for n in stranice:
    url = baza + str(n)
    linkovi += eksport_linkova(url)

print(linkovi)

with open ('database/vesti_iz_hriscanskog_sveta_15/vesti.txt', 'w') as f:
    for link in linkovi:
        f.write(link + '\n')
        