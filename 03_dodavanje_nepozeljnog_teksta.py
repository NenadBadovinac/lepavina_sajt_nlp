# Dodavanje nepozeljnog teksta

import json
import string
import cyrtranslit

naslov = 'ovde prekopiraj naslov'

sadrzaj = '''

ovde prekopiraj sadrzaj


'''

def filtriranje(naslov, sadrzaj):
    
    naslov = list(map(lambda a: a.strip('\u201e'), naslov.split()))
    naslov = list(map(lambda a: a.strip('\u201c'), naslov))
    naslov = list(map(lambda a: cyrtranslit.to_latin(a), naslov))
    naslov = ' '.join(naslov)

    sadrzaj = list(map(lambda a: a.lower(), sadrzaj.split()))
    sadrzaj = list(map(lambda a: a.strip('\u201a'), sadrzaj))
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

    if len(recnik) > 3699:
        raise Exception('BAZA SA NEPOZELJNIM TEKSTOVIMA JE POPUNJENA')
        
        
    naslov, sadrzaj = filtriranje(naslov, sadrzaj)

    recnik[naslov] = sadrzaj
    
    with open('database\\nepozeljni.json', 'w') as f:
        json.dump(recnik, f, indent = 2)



