#učitavanje rečnika svih reči
import json

putanja = "database/recnik.json"
with open(putanja, 'r') as f:
    #recnik koji ima ključ i vrednost: Redbr: [naslov, sadrzaj, tema]
    recnik_svih_objava = json.load(f)    

#rečnik štampa 'posebno' 'sve' 'reči'. 
#print (recnik_svih_objava["1"])

#%% Definisanje klase koja se odnosi na Objavu teksta (Objava)
class Objava:
    #obrazac za pravljenje člana klase koja se zove Objava
    def __init__(self,redbr,naslov,sadrzaj,tema):
        self.redbr=redbr
        self.naslov=naslov
        self.sadrzaj=sadrzaj
        self.tema=tema
        
# sve_objave je lista koja sadrži sve objave koje su u formi koja će se korstiti za ML. 
sve_objave = []

#pošto radimo iteraciju rečnika  potrebno je staviti .items()
for redbr, post_lista in recnik_svih_objava.items():
    #sadržaj objave ćemo joinati.
    sadrzaj = " ".join(post_lista[1])
    #post je objekat klase Objava
    post = Objava(redbr,post_lista[0], sadrzaj, post_lista[2])    
    sve_objave.append(post)


# stampanje objekta: "Objava" po atributima:
#objava=sve_objave[1090]
#print(objava.naslov)

#%% Kreiranje liste koja će sadržavati one teme koje ćemo uspoređivati.
#Potrebno je za svaki post proveriti da li je tema jedna od ove dve i vrati samo postova koje imaju ove teme.
#teme_koje_usporedjujemo = list(filter(lambda post: post.tema=="podviznici_11" or post.tema=="intervjui_9", sve_objave))

#Ovo uljučujemo kada sve katoeriju ali tada treba i novi pickle napraviti
teme_koje_usporedjujemo = sve_objave

# printaj količinu svih objava u listama: sve_objave i objava u teme_koje_usporedjujemo
#print (len(sve_objave),len(teme_koje_usporedjujemo)) 

#%% Machine Learning import biblioteke

from sklearn.model_selection import train_test_split

#deljenje svih postova na one koje su za trening i za testiranje. 
#Algoritam za random će ih jednako promešati i svaki put ćemo dobiti isti random.
train, test = train_test_split(teme_koje_usporedjujemo, test_size=0.30, random_state=1)

#ukupno koliko tekstova imamo za Treniranje, a koliko za Testiranje.
print("Broj objava za treniranje modela: " + str(len(train)))
print("Broj objava za testiranje modela: " + str(len(test)))
print ("Sve objave: " + str(len(teme_koje_usporedjujemo)))
#ukupno koji je redni broj (ID) teksta u listi.
#print(train[1].redbr, test[1].redbr)

#%%

#napraviti listu koja će za svaka post u traning i testing listi dodati sadržaj tog posta
train_sadrzaj=[post.sadrzaj for post in train] 
train_tema=[post.tema for post in train]
test_sadrzaj=[post.sadrzaj for post in test] 
test_tema=[post.tema for post in test]

#print(train_tema[23], test_tema[44])

#%% primena CountVectorized za transformaciju tekstova u postu u jednu tačku u visedimenzionalnom prostoru. 
from sklearn.feature_extraction.text import TfidfVectorizer

# Mašina je prvo radila uniju svih reči u svim tekstovima.
# funkcija koja broji koliko puta se svaka reč iz ukupnog fonda reči pojavljuje u svakom pojedinačnom postu
# Napravljena je unija svih reči i pripisala im je određenu dimenziju.
# Za svai tekss prebrojače sve reči i npr. za reč sunce=734 odredit će koje je mesto u listi. 
# CV - brojač koliko ima kojih reči, ali kda stavim Boolean, binary=True tada štampa samo ono što ima, a ne koliko rputa (1/0)
# Frekvencija - uzima broji koliko puta se koja reč desila i širi se prostor sa vektorima
# Boolean - ima ili nema reši iz vectora. 
# TF_IDF ' uzima frekvencije reči ali sa logaritmima. 
# IDF - eliminiše reči koji se više puta pojaljuju u tekstovima, tim tekstovima daje manju važnost, 
# ako se malo pojavljuje u tekstovima onda im daje veću važnost. 
CV = TfidfVectorizer(use_idf=True)
train_vektori = CV.fit_transform(train_sadrzaj)
test_vektori = CV.transform(test_sadrzaj)

#Klasifikator SVC koji ćemo FItovati prema Train vectorima. Ja imam listu train_vektori i listu tran_tema. 
#Fitovanje: Probaj da nadjes vezu izmedju liste: train_vectori i train_tema.
#Statistiko pitanje: sistem može da nadje oblasti u kojima se nalaze ili Podviznici ili Intervjui 
from sklearn.svm import SVC
klasifikator = SVC(kernel='linear')
klasifikator.fit(train_vektori,train_tema)

#Predvidanje: kakve će vrednosti imati dati vectori iz Test liste.
#hocemo videti u kojem procentru će mašina da pogadja teme.

k=0
for i in range(len(test_tema)):
    stvarna_tema=test_tema[i]
    predvidjena_tema=klasifikator.predict(test_vektori[i])
    if stvarna_tema==predvidjena_tema:
        k+=1
    #print("{}\t{}".format(stvarna_tema,predvidjena_tema[0]))

procenat_uspesnosti=round(k*100/len(test_tema),2)
print("Procenat uspešnosti: " + str(procenat_uspesnosti) + "%")

#%%

import pickle

with open('database\SVM_TfIDF_klasifikator_svi_postovi.pkl','wb') as f:
    pickle.dump(klasifikator,f)

with open('database\TfIDF_testsize_10_svi_postovi.pkl','wb') as f:
    pickle.dump(CV,f)



