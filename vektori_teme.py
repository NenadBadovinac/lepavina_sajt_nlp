
rb_tema = {
        0:'duhovne_pouke',
        1:'intervjui',
        2:'cuda_bozija',
        3:'knjige',
        4:'internet_biblioteka',
        5:'manastirske_novosti',
        6:'pisma',
        7:'pitanja_odgovori',
        8:'podviznici',
        9:'propovedi_ovasilije',
        10:'reportaze',
        11:'vesti_iz_hriscanskog_sveta'}

tema_rb = {
        'duhovne_pouke_6':0,
        'intervjui_9':1,
        'cuda_bozija_10':2,
        'knjige_18':3,
        'internet_biblioteka_8':4,
        'manastirske_novosti_14':5,
        'pisma_20':6,
        'pitanja_odgovori_22':7,
        'podviznici_11':8,
        'propovedi_ovasilije_19':9,
        'reportaze_21':10,
        'vesti_iz_hriscanskog_sveta_15':11}


# vraca naziv teme
def tema(rb):
    return rb_tema[rb]


# vraca trening vektore i teme
def podaci():
  
    # 1 Preuzimanje recnika u formatu redbr:[naslov, reci, tema]
    import json
    import numpy as np

    # format> redbr:[naslov, lista_reci, tema]
    putanja = "database/recnik.json"
    with open(putanja, 'r') as f:
        recnik = json.load(f)


    # 2 Kreiranje liste sadrzaja i tema. Sadrzaj (skup reci -> tekst)
    trening_sadrzaji = []
    teme = []

    for redbr, post_lista in list(recnik.items()):
        if int(redbr) % 10 == 0:
            sadrzaj = " ".join(post_lista[1])
            trening_sadrzaji.append(sadrzaj)
            teme.append(tema_rb[post_lista[2]])

    teme = np.array(teme)


    # 3 Vektorisanje sadrzaja
    from sklearn.feature_extraction.text import TfidfVectorizer

    V = TfidfVectorizer(use_idf = True)
    trening_vektori = V.fit_transform(trening_sadrzaji)
    trening_vektori = trening_vektori.toarray()
    
    return trening_vektori, teme





        
    
