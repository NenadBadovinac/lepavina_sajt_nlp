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
        

    

