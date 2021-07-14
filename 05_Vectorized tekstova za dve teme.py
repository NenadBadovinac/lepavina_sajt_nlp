#učitavanje rečnika svih reči
import json

putanja = "database/recnik.json"
with open(putanja, 'r') as f:
    #recnik koji ima ključ i vrednost: Rgb: [naslov, sadrzaj, tema]
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
#objava=sve_objave[100]
#print(objava.naslov)

#%% Kreiranje liste koja će sadržavati one teme koje ćemo uspoređivati.
#Potrebno je za svaki post proveriti da li je tema jedna od ove dve i vrati samo postova koje imaju ove teme.
teme_koje_usporedjujemo = list(filter(lambda post: post.tema=="podviznici_11" or post.tema=="intervjui_9", sve_objave))

# printaj količinu svih objava u listama: sve_objave i objava u teme_koje_usporedjujemo
print (len(sve_objave),len(teme_koje_usporedjujemo)) 

#%% Machine Learning import biblioteke

from sklearn.model_selection import train_test_split

#deljenje svih postova na one koje su za trening i za testiranje. 
#Algoritam za random će ih jednako promešati i svaki put ćemo dobiti isti random.
train, test = train_test_split(teme_koje_usporedjujemo, test_size=0.10, random_state=1)

#ukupno koliko tekstova imamo za Treniranje, a koliko za Testiranje.
print(len(train), len(test))

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
from sklearn.feature_extraction.text import CountVectorizer

# Mašina je prvo radila uniju svih reči u svim tekstovima.
# funkcija koja broji koliko puta se svaka reč iz ukupnog fonda reči pojavljuje u svakom pojedinačnom postu
# Napravljena je unija svih reči i pripisala im je određenu dimenziju.
# Za svai tekss prebrojače sve reči i npr. za reč sunce=734 odredit će koje je mesto u listi. 
CV = CountVectorizer()
train_vektori = CV.fit_transform(train_sadrzaj)
test_vektori = CV.fit_transform(test_sadrzaj)

#ispis 476 tekstova koje smo odvojili za trenitn, drugi član je reč u ukupnom rečniku, a traći član je frekvenijija. 
# za svaki tekst (0) i za svaku reč u tekstu iz rečnika svih reči (CV funkcija) pojavila se 15 puta. npr: (0, 13502)	15
# ispis 235 tekstova koje smo odvojili u testiranje

print(train_vektori)
#%%
print(test_vektori)
#%%Print vectora samo jednog teksta iz rečnika za Testiranje
print(test_vektori[0])

# napravimo smo tekstove u tačke ,a sada primennjujemo neke algoritma. 
        
