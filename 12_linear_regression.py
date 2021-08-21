#hipoteza je h(x) = a + bx0 + cx1.. 
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

def r2(Y_ts, Y_pred):
    g = np.sum((Y_ts - Y_pred)**2)#suma kvadrata odstupanja ocekivanih vrednosti od stvarnih
    y = np.sum((Y_ts - np.mean(Y_ts, axis=0))**2)#suma kvadrata odstupanja stvarnih vrednosti od srednje stvarne vrednosti
    r = 1 - (g/y)#vrednosti od 0 - 1 (1 je najbolje poklapanje)
    return r

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
        return h

if __name__ == '__main__':
    
    from sklearn.model_selection import train_test_split
    from sklearn import datasets
    
    X, Y = datasets.make_regression(
        n_samples = 100,#broj tacak
        n_features = 1,#broj promenljivih
        noise = 20,#koliku standardnu devijaciju da primenis
        random_state = 1)

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

    uspesnost = r2(Y_ts, predictions)
    print('Uspesnost', round(uspesnost, 2))

    #srednja kvadratna greska
    def MSE(Y_tr, Y_pr):
        return np.mean((Y_ts - Y_pr) ** 2)
    
    mse = MSE(Y_tr, predictions)
    print('MSE', round(mse))

    
    #matplotlib
    import matplotlib.pyplot as plt
    
    y_pred_line = R.predict(X)
    cmap = plt.get_cmap("viridis")
    fig = plt.figure(figsize=(8, 6))
    m1 = plt.scatter(X_tr, Y_tr, color=cmap(0.9), s=10)
    m2 = plt.scatter(X_ts, Y_ts, color=cmap(0.5), s=10)
    plt.plot(X, y_pred_line, color="black", linewidth=1, label="Prediction")
    plt.show()



    
