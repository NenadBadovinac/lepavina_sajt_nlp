#logistic regression je kvalifikator
#sva stvarna resenja su 0 ili 1
#podesavamo parametre da cost function bude minimalan
#modelu se pripisuje neka vrednost izmedju 0 i 1
#od svake hipoteticke funkcije pravi se sigmoidna funkcija 1/(1+e^(-h(x))) 
#hipoteza je h(x) = a + bx0 + cx1..
#1)h=0 -> y=0.5 2)h>0 -> 0.5 < y < 1 3)h<0 -> 0 < y < 0.5
#resenje je brojna vrednost za koju smatramo da linearno zavisi od promenjljivih
#dat je jednak broj kolona za promenljive i rezultate
#h(x) linearno zavisi od promenljivih
#za jednu promenljivu h je linija, za dve je povrs itd..
#kada su ostale promenljive fiksirane h(x) = fixiran_deo + ax (linerano se menja sa x)
#zelimo da provucemo liniju, povrs ili n-dim povrs najbolje kroz postojece tacke
#mozemo odrediti razlike izmedju stvarne i predvidjene vrednosti
#zelimo da imamo veci broj manjih gresaka (slucaj kada prava prolazi kroz sredinu tacaka)
#J(tetas) = 1/2m x sum(hi(x) - yi)^2
#m je broj tacaka (redova u fajlu)
#J(teta) ima oblik zvona sa minimumom J(teta)
#dJ/dteta = 1/m x sum(hi(x) - yi)xi
#dJ/dteta_nula = 1/m x sum(hi(x) - yi)
#u svakoj iteraciji:
#teta = teta - alfa x 1/m x sum(hi(x) - yi)xi
#teta_nula = teta_nula - alfa x 1/m x sum(hi(x) - yi)
#ako je suma pozitivna h(x) je vece od y i treba smanjiti teta (i obrnuto) - desna strana zvona
#ako je dJ/dteta veliko i promena je velika (srazmerna izvodu)
# sto smo blize minimumu, promena se sporije odvija

import numpy as np

class LR:
    def __init__(self, learning_rate = 0.001, n_iters = 1000):
        self.lr = learning_rate
        self.n_iters = n_iters
        self.weights = None
        self.bias = None

    def fit(self, X_tr, Y_tr):
        n_samples, n_features = X_tr.shape

        self.weights = np.zeros(n_features)#koeficijenti za svaku kolonu
        self.bias = 0#slobodan koeficijent

        for _ in range(self.n_iters):#fitujemo koeficijente onoliko puta koliki je zadat broj iteracija

            h = np.dot(X_tr, self.weights) + self.bias
            Y_pr = self._sigmoid(h)
            
            db = (1 / n_samples) * np.sum(h - Y_tr)
            dw = (1 / n_samples) * np.dot(X_tr.T, (h - Y_tr))
            #X.T transponuje matricu
            #u jednom se redu sada nalaze vrednosti za jednu promenljivu
            #svakoj koloni sada odgovara jedna tacka (broj redova je broj promenljivih)
            #dot - svaki clan u redu se mnozi sa odgovarajucom razlikom predvidjene i stvarne vrednosti 
            #sabiramo svaki takav red i dobijamo listu sa onoliko clanova koliko ima promenljivih

            self.bias -= self.lr * db
            self.weights -= self.lr * dw
            
    def predict(self, X):
        h = np.dot(X, self.weights) + self.bias
        #dot ce svaki clan matrice da pomnozi odgovarajucim teta i da sabere takav red
        #svakom redu dodamo i slobodan koeficijent - odsecak
        #dobijamo listu sa n predvidjenih y
        Y_pr = self._sigmoid(h)
        Y_cls = [1 if i > 0.5 else 0 for i in Y_pr]
        return np.array(Y_cls)

    def _sigmoid(self, h):
        return 1 / (1 + np.exp(-h))

if __name__ == '__main__':
    
    from sklearn.model_selection import train_test_split
    from sklearn import datasets
    
    def uspesnost(Y_tr, Y_cls):
        uspesnost = np.sum(Y_tr == Y_cls) / len(Y_tr)
        return uspesnost

    bc = datasets.load_breast_cancer()
    X, Y = bc.data, bc.target

    X_tr, X_ts, Y_tr, Y_ts = train_test_split(
        X,
        Y,
        test_size = 0.2,
        random_state = 1)

    learning_rate = 0.001
    n_iters = 1000

    R = LR(learning_rate, n_iters)
    R.fit(X_tr, Y_tr)

    predictions = R.predict(X_ts)

    uspeh = uspesnost(Y_ts, predictions)
    print('Uspesnost', round(uspeh, 2))





    
