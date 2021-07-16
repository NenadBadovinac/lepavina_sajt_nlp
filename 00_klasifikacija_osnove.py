import json
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer


# 1 Preuzimanje recnika u formatu redbr:[naslov, reci, tema]

putanja = "database/recnik.json"
with open(putanja, 'r') as f:
    recnik = json.load(f)    


# 2 Definisemo klasu Objava
class Objava:
    def __init__(self, redbr, naslov, sadrzaj, tema):
        self.redbr = redbr
        self.naslov = naslov
        self.sadrzaj = sadrzaj
        self.tema = tema
        

# 3 Pravimo listu objekata klase Objava. Sadrzaj (skup reci -> tekst)

objave = []

for redbr, post_lista in recnik.items():
    sadrzaj = " ".join(post_lista[1])
    post = Objava(redbr, post_lista[0], sadrzaj, post_lista[2])    
    objave.append(post)


# 4 Delimo listu na uzorke na kojima cemo traziti algoritam i na one na kojima cemo testirati model

train, test = train_test_split(objave, test_size=0.30, random_state=1)

train_sadrzaj = [post.sadrzaj for post in train] 
train_tema = [post.tema for post in train]
test_sadrzaj = [post.sadrzaj for post in test] 
test_tema = [post.tema for post in test]


# 5 CV je objekat klase koji radi vektorizaciju.
# fit_transform - na osnovu svih reci svaki train tekst se pretvara u vektor
# transform - svaki test tekst se na osnovu train modela pretvara u vektor
  
CV = TfidfVectorizer(use_idf = True)
train_vektori = CV.fit_transform(train_sadrzaj)
test_vektori = CV.transform(test_sadrzaj)


# 6 klasifikator je objekat klase algoritma
# fit - trazi n-dimenzionalne vektorske oblasti koje odgovaraju odredjenoj temi

from sklearn.svm import SVC
klasifikator = SVC(kernel='linear')
klasifikator.fit(train_vektori, train_tema)


# 7 predict - predvidja temu na osnovu lokacije vektora u n - dimenzionalnom prostoru
# Testiramo model na osnovu poklapanja sa stvarnom temom
k=0
for i in range(len(test_tema)):
    stvarna_tema = test_tema[i]
    predvidjena_tema = klasifikator.predict(test_vektori[i])
    if stvarna_tema == predvidjena_tema:
        k+=1
    #print("{}\t{}".format(stvarna_tema,predvidjena_tema[0]))

procenat_uspesnosti = round(k*100/len(test_tema),2)
print("Procenat uspešnosti: " + str(procenat_uspesnosti) + "%")


'''
with open('database\SVM_TfIDF_klasifikator_svi_postovi.pkl','wb') as f:
    pickle.dump(klasifikator,f)

with open('database\TfIDF_testsize_10_svi_postovi.pkl','wb') as f:
    pickle.dump(CV,f)

'''

