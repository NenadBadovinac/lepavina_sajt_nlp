import json
import string

def recnik_linkova(lista_tema):

    #definisanje praznog rečnika
    t_recnik = {}
    
    for tema in lista_tema:
#za svaku temu definisanje prazne liste linkiva, i onda smo za svaki link 
        lista_linkova = []
        #proveri u kojoj su formi zabelezeni linkovi ja sam otvorio link faklova i za svaki link u fajlu 
        putanja = "database/" + tema + '/' +"linkovi.txt"
        with open(putanja, 'r') as f:  
            for link in f:
                link = link.rstrip('\n')
                link = link[14:]
                lista_linkova.append(link)
# dobio sam sve linkove u jednoj temi i onda sam i onda sam za lista_linkova =  [1234], 1234, 1313,, tema= duhovne_pouke

        t_recnik[tema] = lista_linkova
# dobio sam {'duhovne_pouke': [1234, 23245,] }
        
    return t_recnik


def recnik_sadrzaj(t_recnik):

    recnik = {}
    
    for tema, linkovi in t_recnik.items():
        for rgb in linkovi:
            putanja = "database/" + tema + '/' + rgb + ".json"
            with open(putanja, 'r') as f:
                data = json.load(f)           
            
            naslov = data['naslov']
            naslov = list(map(lambda a: a.strip('\u201e'), naslov.split()))
            naslov = list(map(lambda a: a.strip('\u201c'), naslov))
            naslov = ' '.join(naslov)

            sadrzaj = data['sadrzaj']
            sadrzaj = list(map(lambda a: a.strip('\u201a'), sadrzaj))
            sadrzaj = list(map(lambda a: a.strip('\u201e'), sadrzaj))
            sadrzaj = list(map(lambda a: a.strip('\u201c'), sadrzaj))
            sadrzaj = list(map(lambda a: a.strip('\u201d'), sadrzaj))
            sadrzaj = list(map(lambda a: a.strip('\u2026'), sadrzaj))
            sadrzaj = list(map(lambda a: a.strip(string.punctuation + string.whitespace), sadrzaj))

            def kratke_reci(rec):
                if len(rec) > 3 or rec == 'bog' or rec == 'oče' or rec == 'oce' or rec == 'mir' or rec == 'duh' or rec == 'sv.' or rec == 'car' or rec == 'sin' or rec == 'pop' or rec == 'moj':
                    return rec
            
            sadrzaj = list(filter(kratke_reci, sadrzaj))
  
            recnik[rgb] = [naslov, sadrzaj, tema]
            
    return recnik

#markira pocetak izvrsavanja koda
if __name__ == '__main__':

    lista_tema = ['duhovne_pouke_6','intervjui_9','cuda_bozija_10', 'knjige_18', 'internet_biblioteka_8', 'manastirske_novosti_14', 'pisma_20', 'pitanja_odgovori_22', 'podviznici_11', 'propovedi_ovasilije_19', 'reportaze_21', 'vesti_iz_hriscanskog_sveta_15']
    t_recnik = recnik_linkova(lista_tema)
    recnik = recnik_sadrzaj(t_recnik)

    with open("database/recnik_sort.json", "w") as f:
        json.dump(recnik, f, indent=2, sort_keys=True)
