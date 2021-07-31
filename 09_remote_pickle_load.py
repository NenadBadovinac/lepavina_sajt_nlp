from io import BytesIO
import cyrtranslit
import string

sadrzaj = '''

Na VII. nedjelju po Duhovima, 11. srpnja 2021., u župnoj crkvi sv. Pavla u Kukljici na otoku Ugljanu, nadbiskup košićki i član Vrhovnog suda Apostolske signature u Rimu, vladika Cyril Vasil DI, služio je svetu liturgiju zajedno s tajnikom o. Martinom Mrazom, zadarskim dušobrižnikom o. Marjanom Jeftimovim, svećenikom voditeljem ureda za medije Košićke eparhije Tomažom i đakonom Livijom Marijanom. Pjevali su pjevači Grkokatoličkog pastoralnog centra Zadar. Vladika Vasil, koji je bio i višegodišnji tajnik Kongregacije za Istočne Crkve, provodi ljetni odmor na otoku Ugljanu. U homiliji je potaknuo vjernike na povjerenje u Krista koji uvijek sve čini na dobrobit cjelovitog čovjeka, imajući uvijek kao krajnji ciolj njegovo vječno spasenje.
'''

def filtriranje(sadrzaj):

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

    sadrzaj = [' '.join(sadrzaj)]
     
    return sadrzaj


if __name__ == '__main__':

    import requests
    import pickle
    
    sadrzaj = filtriranje(sadrzaj)
    
    link = 'https://github.com/NenadBadovinac/lepavina_sajt_nlp/blob/nlp_poredjenje/database/vektorizator.pkl?raw=true'
    file = BytesIO(requests.get(link).content)
    V = pickle.load(file)

    link = 'https://github.com/NenadBadovinac/lepavina_sajt_nlp/blob/nlp_poredjenje/database/klasifikator.pkl?raw=true'
    file = BytesIO(requests.get(link).content)
    klasifikator = pickle.load(file)

    vektor = V.transform(sadrzaj)
    predvidjena_pozeljnost = klasifikator.predict(vektor)

    print('Tekst je:', predvidjena_pozeljnost[0].capitalize())



















