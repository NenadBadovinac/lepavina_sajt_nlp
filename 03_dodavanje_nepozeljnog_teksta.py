# Dodavanje nepozeljnog teksta

import json
import string
import cyrtranslit

#prekopirajte naslov i sadrzaj dole

naslov = 'VLADIKA CYRIL VASIL SLUŽIO LITURGIJU U KUKLJICI NA OTOKU UGLJANU'

sadrzaj = '''
Na VII. nedjelju po Duhovima, 11. srpnja 2021., u župnoj crkvi sv. Pavla u Kukljici na otoku Ugljanu, nadbiskup košićki i član Vrhovnog suda Apostolske signature u Rimu, vladika Cyril Vasil DI, služio je svetu liturgiju zajedno s tajnikom o. Martinom Mrazom, zadarskim dušobrižnikom o. Marjanom Jeftimovim, svećenikom voditeljem ureda za medije Košićke eparhije Tomažom i đakonom Livijom Marijanom. Pjevali su pjevači Grkokatoličkog pastoralnog centra Zadar. Vladika Vasil, koji je bio i višegodišnji tajnik Kongregacije za Istočne Crkve, provodi ljetni odmor na otoku Ugljanu. U homiliji je potaknuo vjernike na povjerenje u Krista koji uvijek sve čini na dobrobit cjelovitog čovjeka, imajući uvijek kao krajnji ciolj njegovo vječno spasenje.
'''
def filtriranje(naslov, sadrzaj):

    naslov = list(map(lambda a: a.strip('\u201e'), naslov.split()))
    naslov = list(map(lambda a: a.strip('\u201c'), naslov))
    naslov = list(map(lambda a: cyrtranslit.to_latin(a), naslov))
    naslov = ' '.join(naslov)
    
    sadrzaj = list(map(lambda a: a.strip('\u201a'), sadrzaj.split()))
    sadrzaj = list(map(lambda a: a.strip('\u201e'), sadrzaj))
    sadrzaj = list(map(lambda a: a.strip('\u201c'), sadrzaj))
    sadrzaj = list(map(lambda a: a.strip('\u201d'), sadrzaj))
    sadrzaj = list(map(lambda a: a.strip('\u2026'), sadrzaj))
    sadrzaj = list(map(lambda a: a.strip(string.punctuation + string.whitespace), sadrzaj))
    sadrzaj = list(map(lambda a: cyrtranslit.to_latin(a), sadrzaj))


    def kratke_reci(rec):
        if len(rec) > 3 or rec in ['bog',
                                   'oče',
                                   'oce',
                                   'mir',
                                   'duh',
                                   'sv.',
                                   'car',
                                   'sin',
                                   'pop',
                                   'moj']:
            return rec
            
    sadrzaj = list(filter(kratke_reci, sadrzaj))

    print('Broj reci:', len(sadrzaj))
      
    return naslov, sadrzaj


if __name__ == '__main__':
    
    with open('database\\nepozeljni.json', 'r') as f:
        recnik = json.load(f)
        
    naslov, sadrzaj = filtriranje(naslov, sadrzaj)

    recnik[naslov] = sadrzaj
    
    with open('database\\nepozeljni.json', 'w') as f:
        json.dump(recnik, f, indent = 2)



