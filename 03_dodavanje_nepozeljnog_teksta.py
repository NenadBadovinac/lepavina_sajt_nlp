# Dodavanje nepozeljnog teksta

import json
import string


def filtriranje(naslov, sadrzaj):
            
    naslov = list(map(lambda a: a.strip('\u201e'), naslov.split()))
    naslov = list(map(lambda a: a.strip('\u201c'), naslov))
    naslov = ' '.join(naslov)

    sadrzaj = list(map(lambda a: a.strip('\u201a'), sadrzaj.split()))
    sadrzaj = list(map(lambda a: a.strip('\u201e'), sadrzaj))
    sadrzaj = list(map(lambda a: a.strip('\u201c'), sadrzaj))
    sadrzaj = list(map(lambda a: a.strip('\u201d'), sadrzaj))
    sadrzaj = list(map(lambda a: a.strip('\u2026'), sadrzaj))
    sadrzaj = list(map(lambda a: a.strip(string.punctuation + string.whitespace), sadrzaj))

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
            
    return naslov, sadrzaj


def main(recnik):
    print('\nDA PREKINETE SA UNOSOM STISNITE ENTER')   
    while True:
        naslov = input('\nPREKOPIRAJTE NASLOV:\n>>')
        if len(naslov) < 2:
            break
        sadrzaj = input('\nPREKOPIRAJTE SADRZAJ:\n>>')
        naslov, sadrzaj = filtriranje(naslov, sadrzaj)
        recnik[naslov] = sadrzaj    
    return recnik


if __name__ == '__main__':
    
    with open('database\\nepozeljni.json', 'r') as f:
        recnik = json.load(f)
        
    recnik = main(recnik)
    
    with open('database\\nepozeljni.json', 'w') as f:
        json.dump(recnik, f, indent = 2)



