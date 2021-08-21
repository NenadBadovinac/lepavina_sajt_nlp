'''
Sadrzaj se filtrira od praznina, znakova i
nepotrebnih reci, pretvara u TfIdf vektor
i kvalifikuje prema vec konstruisanom modelu.
'''

def filtriranje(sadrzaj):

    from io import BytesIO
    import cyrtranslit
    import string    
    import requests
    import pickle
    
    # od sadrzaja se pravi lista reci
    # sva slova se prevode u mala
    sadrzaj = list(map(lambda a: a.lower(), sadrzaj.split()))

    # skidaju se neki posebni znakovi
    sadrzaj = list(map(lambda a: a.strip('\u201a'), sadrzaj))
    sadrzaj = list(map(lambda a: a.strip('\u201e'), sadrzaj))
    sadrzaj = list(map(lambda a: a.strip('\u201c'), sadrzaj))
    sadrzaj = list(map(lambda a: a.strip('\u201d'), sadrzaj))
    sadrzaj = list(map(lambda a: a.strip('\u2026'), sadrzaj))
    
    # skidaju se interpunkcije i praznine
    sadrzaj = list(map(lambda a: a.strip(string.punctuation + string.whitespace), sadrzaj))
    
    # ako je sadrzaj na cirilici pretvara se u latinicu 
    sadrzaj = list(map(lambda a: cyrtranslit.to_latin(a), sadrzaj))

    # fitriranje kratkih reci (ispod 4 slova), uz dole navedene izuzetke
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

    # pikle fajl - vektorizator postavljen na githubu se ucitava
    link = 'https://github.com/NenadBadovinac/lepavina_sajt_nlp/blob/nlp_poredjenje/database/vektorizator.pkl?raw=true'
    file = BytesIO(requests.get(link).content)
    V = pickle.load(file)

    # pikle fajl - klasifikator postavljen na githubu se ucitava
    link = 'https://github.com/NenadBadovinac/lepavina_sajt_nlp/blob/nlp_poredjenje/database/klasifikator.pkl?raw=true'
    file = BytesIO(requests.get(link).content)
    klasifikator = pickle.load(file)

    # dati sadrzaj se prevodi u vektor (sadrzaj mora biti lista) 
    vektor = V.transform(sadrzaj)

    # predvidja se pozelljnost na osnovu ucitanog klasifikatora
    predvidjena_pozeljnost = klasifikator.predict(vektor)

    return predvidjena_pozeljnost[0].capitalize(), predvidjena_pozeljnost





















