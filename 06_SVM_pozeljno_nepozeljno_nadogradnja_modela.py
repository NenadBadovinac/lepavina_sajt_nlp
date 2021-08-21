'''
1.
- formirana su dva python recnika sacuvana kao json fajlovi
- prvi sadrzi pozeljne, a drugi nepozeljne tekstove
- relativne putanje su im:
    pozeljni - "database/recnik.json"
    nepozeljni - "database/nepozeljni.json"
- oba sadrze naslov i sadrzaj teksta
- recnik.json sadrzi i temu (postoji 12 tema)
- json fajlovi su otvoreni i ucitani (prevedeni u python recnik) da bi se nad njima formirao model

2.
- formirana je klasa Objava koja poseduje tri atributa relevantna za nas model:
    - naslov
    - sadrzaj
    - pozeljnost
    
3.
- svakom tekstu iz dva recnika pripisan je odgovarajuci objekat klase Objava
- svim objektima vezanim za recnik.json pripisana je pozeljnost 'pozeljan'
- svim objektima vezanim za nepozeljni.json pripisana je pozeljnost 'nepozeljan'
- svim objektima je pripisan odgovarajuci naslov
- svim objektima je pripisan odgovarajuci sadrzaj dobijen spajanjem reci iz odgovarajuce liste reci u recniku
- svi objekti klase Objava su dodati u zajednicku listu - objave

4.
- pokrenuta je funkcija splitovanje koja ima dva parametra
    - spliter (udeo tekstova (objekata klase Objava) za trening i test)
    - list objave nad kojom ce se izvrsiti dalje operacije

5.
- tekstovi su podeljeni u zadatom odnosu (0.8 - trening, 0.2 - test)
- ovaj pocetni odnos je zgodan da bi se dobila realna slika uspesnosti
- sa vecim brojem tekstova udeo onih za trening se moze povecati da bi se dobio bolji model
 (ako znamo da algoritam radi, testiranje nam nije bitno)
- izbor tekstova za trening i testiranje je nasumican (ne prvoh 80% za trening),
  ali uvek prati isti algoritam
 (ovo je neophodno kod poredjenja razlicitih algoritama i parametara za kvalifikaciju,
  ali nakon izbora modela nije toliko bitno)
- napravljene su respektivne liste sa sadrzajuma i pozeljnostima
 (npr 33 clan liste train_sadrzaj ima respektivnu pozeljnost na 33 mestu u listi train_pozeljnost)
 
- uvedena je klasa TfidfVectorizer iz python scikit-learn biblioteke
- definisan je objekat klase koga smo nazvali V
- definisali smo parametar za dati objekat -> use_idf = True
- nad datim objektom (V) klase TfidfVectorizer, izvrsili smo funkciju fit_transform sa parametrom (train_sadrzaj)
- fit_transform:
    - napravljen je skup svih reci iz sadrzaja svih objekata za trening
    - za svaki objekat (trening tekst), napravljen je vektor-lista koji sadrzi
      onoliko mesta-dimenzija koliko ima razlicitih reci u skupu svih reci
    - svakoj reci odgovara odredjeno mesto u vektoru-listi
    - rec se ili pojavljuje, ili ne pojavljuje
    - rec se pojavljuje:
        - Tf = 1+log(f) - f je koliko se puta data rec pojavljuje u datom tekstu
        - idf = log(N/n) - N je broj tekstova za trening, n je u koliko se tekstova data rec pojavljuje
        - Tfidf = Tf x idf = (1+log(f)) x log(N/n)
        - oba logaritma su sa osnovom 2
        - Tf pokazuje koliko je data rec vazna u tekstu (sto je ima vise u tekstu Tf je veci (ali ne linearno..))
        - idf pokazuje koliko je data rec uopste vazna (sto je ima vise u tekstovima idf je manji)
        - pr neki veznik ima ima idf = 0 jer se svuda pojavljuje, pa je ta rec nebitna kao da je nema (Tfidf = 0)
    - rec se ne pojavljuje:
        - Tf = 0 (samim tim i Tfidf)
    - sve vrednosti se normalizuju Tfidf(novo) = Tfidf(staro)/Tfidf(max)
    - Tfidf se odredjuje za svaki svaku rec svakog train objekta i zapisuje u njemu odgovarajuci vektor
    - sada imamo listu train_vektori koja poseduje onoliko podlista-vektora koliko ima train objekata
- klasa V sada sadrzi obrazac kako da pretvori bilo koji drugi tekst u vektor
- obrazac podrazumeva vektor sa prethodno utvrdjenim dimenzijama gde svakoj odgovara neka rec
- obrazac takodje podrazumeva i prethodno utvrdjene idf vrednosti za svaku rec
- nad datim objektom (V) klase TfidfVektorizer, vrsimo funkciju transform
- transform pripisuje svakom test_sadrzaju vektor po istom obrascu koji je koriscen za train_sadrzaj
- dati obrazac se cuva u pickle fajlu kao vektorizator

6.
- nad grupom od cetiri liste (train_vektori - train_pozeljnost, test_vektori- test_pozeljnost)
  vrsi se funkcija optimizator
- importovana je klasa SVC (support vector machines)
- definisan je objekat klase SVC sa parametrima koji se ticu nacina razgranicenja i brzine nadogradnje modela
- SVC je tekst klasifikator koji radi tako sto pokusava da otkrije dimenzije po kojima se
  razlicito kvalifikovani objekti razlikuju (npr odredjeni tip teksta ne koristi odredjenu rec)
- klasifikator.fit trazi model (podesava parametre SVC algoritma) tako da najbolje klasifikuje objekte
- objekti za trening su vec klasifikovani i SVC ima cilj da proba dimenzije gde postoje razgranicenja
- tako dobijeni klasifikator se snima kao pickle fajl
- klasifikator.predict(test_vektori) primenjuje klasifikaciju nad test_vektorima i klasifikuje prema pozeljnosti
- kako za svaki test objekat vec znamo pozeljnost mozemo odrediti uspesnost kao broj_pogodaka/broj_testiranih
'''

import pickle

# 5 Splitovanje i TfIdf Vektorizacija

def splitovanje(spliter, objave):
    
    train, test = train_test_split(objave, test_size = spliter, random_state=1)

    train_sadrzaj = [post.sadrzaj for post in train] 
    train_pozeljnost = [post.pozeljnost for post in train]
    test_sadrzaj = [post.sadrzaj for post in test] 
    test_pozeljnost = [post.pozeljnost for post in test]

    V = TfidfVectorizer(use_idf = True)
    train_vektori = V.fit_transform(train_sadrzaj)
    test_vektori = V.transform(test_sadrzaj)

    with open('database\\vektorizator.pkl','wb') as f:
        pickle.dump(V, f)

    komplet = [train_vektori, train_pozeljnost, test_vektori, test_pozeljnost]
   
    uspeh = optimizator(komplet)
    print ("Uspesnost:", round(uspeh*100, 2), "%")

       
# 6 Smimanje klasifikatora 

def optimizator(komplet):

    #jezgro = 'sigmoid'
    jezgro = 'linear'
    # regulatore mozes menjati od 1.0 - 1.5 (1.0 je default)
    regulator = 1.5

    train_vektori = komplet[0]
    train_pozeljnost = komplet[1]
    test_vektori = komplet[2]
    test_pozeljnost = komplet[3]
       
    klasifikator = SVC(kernel = jezgro, C = regulator)
    klasifikator.fit(train_vektori, train_pozeljnost)

    with open('database\\klasifikator.pkl','wb') as f:
        pickle.dump(klasifikator, f)
        
    predvidjeno = klasifikator.predict(test_vektori)
    
    def uspesnost(y_test, y_pred):
        uspesnost = np.sum(y_test == y_pred) / len(y_test)
        return uspesnost

    uspeh = uspesnost(test_pozeljnost, predvidjeno)

    for i in range(len(test_pozeljnost)):
        print(test_pozeljnost[i], predvidjeno[i])
    
    return uspeh
    

    
# 0 Start programa
if __name__ == '__main__':

    
    # 1 Preuzimanje pozeljnog i nepozeljnog recnika u formatu redbr:[naslov, reci, tema]
    import json

    # format> redbr:[naslov, lista_reci, tema]
    putanja = "database/recnik.json"
    with open(putanja, 'r') as f:
        pozeljni = json.load(f)
        
    # format> naslov:lista_reci
    putanja = "database/nepozeljni.json"
    with open(putanja, 'r') as f:
        nepozeljni = json.load(f)

        
    # 2 Definisanje klase Objava
    class Objava:
        def __init__(self, naslov, sadrzaj, pozeljnost):
            self.naslov = naslov
            self.sadrzaj = sadrzaj
            self.pozeljnost = pozeljnost
            

    # 3 Kreiranje liste objekata klase Objava. Sadrzaj (skup reci -> tekst)
    objave = []

    for redbr, post_lista in list(pozeljni.items())[:len(nepozeljni)]:
        sadrzaj = " ".join(post_lista[1])
        post = Objava(post_lista[0], sadrzaj, 'pozeljan')    
        objave.append(post)

    for naslov, sadrzaj in nepozeljni.items():
        sadrzaj = " ".join(sadrzaj)
        post = Objava(naslov, sadrzaj, 'nepozeljan')    
        objave.append(post) 

    
    # 4 Uvodjenje ML biblioteka i definisanje koriscenog splita
    from sklearn.model_selection import train_test_split
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.svm import SVC
    import numpy as np

    #parametar vremenom podesiti na 0.1 (sa vecim udelom nepozeljnih tekstova..)
    spliter = 0.2

    splitovanje(spliter, objave)
        

    

