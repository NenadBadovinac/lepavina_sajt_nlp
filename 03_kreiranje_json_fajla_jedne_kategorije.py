'''
naslov_1 - sadrzaj_1 - tema_1
naslov_2 - sadrzaj_2 - tema_1
.......

{id1:('naslov_1', sadrzaj_1, 'tema_1'), id2}
{'tema_1':[22, 333, 543], tema_2:[]}

zadanca: narpaviti json fajl koji ce sve tekstove staviti u jedan fajl zajedno. 

'

lista tema = ['duhovne_pouke','','']

for tema in lista_tema:
    1. izvuces linkove u listu
    2. t_recnik[tema] = lista


for tema, linkovi in t_recnik.items():
    uradi kod dole

'''

import json
import string

lista_linkova = []

with open("database/cuda_bozija_10/cuda_bozija.txt", 'r') as f:  
    for link in f:
        link = link.rstrip('\n')
        link = link[14:]
        lista_linkova.append(link)
        
   
       
recnik = {}
'''
teme = {'folder sa temom': [linkovi]}
for tema, lista in teme.items():
    
'''

for i in lista_linkova:
        
    rgb = i
    
    putanja = "database/cuda_bozija_10/" + rgb + ".json"
    
    with open(putanja, 'r') as f:
            data = json.load(f)
    
    
    # \u201c
    # \u201e
    
    def kratke_reci(rec):
        if len(rec) > 3 or rec == 'bog':
            return rec
    
    sadrzaj = data['sadrzaj']
    naslov = data['naslov']
    
    sadrzaj = list(map(lambda a: a.strip('\u201e'), sadrzaj))
    sadrzaj = list(map(lambda a: a.strip('\u201c'), sadrzaj))
    sadrzaj = list(map(lambda a: a.strip(string.punctuation + string.whitespace), sadrzaj))
    sadrzaj = list(filter(kratke_reci, sadrzaj))
    
    naslov = list(map(lambda a: a.strip('\u201e'), naslov.split()))
    naslov = list(map(lambda a: a.strip('\u201c'), naslov))
    naslov = ' '.join(naslov)
    
    recnik[rgb] = [naslov, sadrzaj, 'Cuda_bozja']

#print(recnik)

for rgb, podaci in recnik.items():
    print(podaci[1])

with open("database/cuda_bozija_10/recnik_cuda_bozija.json", "w") as f:
    json.dump(recnik, f, indent=2)