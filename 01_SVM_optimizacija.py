

# 6 Splitovanje i TfIdf Vektorizacija
def splitovanje(split, kombinacije):
    
    train, test = train_test_split(objave, test_size = split, random_state=1)

    train_sadrzaj = [post.sadrzaj for post in train] 
    train_tema = [post.tema for post in train]
    test_sadrzaj = [post.sadrzaj for post in test] 
    test_tema = [post.tema for post in test]

    CV = TfidfVectorizer(use_idf = True)
    train_vektori = CV.fit_transform(train_sadrzaj)
    test_vektori = CV.transform(test_sadrzaj)

    komplet = [train_vektori, train_tema, test_vektori, test_tema]

    for kombo in kombinacije:
        kombo, uspeh = optimizator(kombo, komplet)
        print ("Uspesnost za:", kombo, round(uspeh*100,2), "%")


        
# 7 Odredjivanje uspesnosti za razlicite kombinacije kernela i regulatora
def optimizator(kombo, komplet):

    jezgro = kombo[0]
    regulator = kombo[1]

    train_vektori = komplet[0]
    train_tema = komplet[1]
    test_vektori = komplet[2]
    test_tema = komplet[3]
       
    klasifikator = SVC(kernel = jezgro, C = regulator)
    klasifikator.fit(train_vektori, train_tema)
        
    predvidjeno = klasifikator.predict(test_vektori)
    
    def uspesnost(y_test, y_pred):
        uspesnost = np.sum(y_test == y_pred) / len(y_test)
        return uspesnost

    uspeh = uspesnost(test_tema, predvidjeno)
    return kombo, uspeh
    

    
# 0 Start programa
if __name__ == '__main__':

    
    # 1 Preuzimanje recnika u formatu redbr:[naslov, reci, tema]
    import json

    putanja = "database/recnik.json"
    with open(putanja, 'r') as f:
        recnik = json.load(f)    


    # 2 Definisanje klase Objava
    class Objava:
        def __init__(self, redbr, naslov, sadrzaj, tema):
            self.redbr = redbr
            self.naslov = naslov
            self.sadrzaj = sadrzaj
            self.tema = tema
            

    # 3 Kreiranje liste objekata klase Objava. Sadrzaj (skup reci -> tekst)
    objave = []

    for redbr, post_lista in recnik.items():
        sadrzaj = " ".join(post_lista[1])
        post = Objava(redbr, post_lista[0], sadrzaj, post_lista[2])    
        objave.append(post)


    # 4 Kreiranje kombinacija (oblik funkcije, penal)
    from itertools import product
    
    jezgra = ['linear','rbf','sigmoid']
    regulatori = [0.5, 0.8, 1.0, 1.2, 1.5]
    
    # 5 Uvodjenje razlicitih splitera
    from sklearn.model_selection import train_test_split
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.svm import SVC
    import numpy as np
    
    spliteri =[0.3, 0.2, 0.1]
    
    for split in spliteri:
        print('\nUdeo tekstova za testiranje:', split)
        print('--------------------------------')
        kombinacije = product(jezgra, regulatori)
        splitovanje(split, kombinacije)
        

    

