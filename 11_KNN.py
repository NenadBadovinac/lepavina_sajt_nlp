#KNN (K Nearest Neighbors)- trazi distance od svih tacaka, bira k najblizih i trazi koji je tip tacaka najzastupjeniji u tih k

from collections import Counter
import numpy as np

def rastojanje(v1, v2):
    return np.sqrt(np.sum((v1 - v2) ** 2))

class KNN:
    def __init__(self, k=3):
        self.k = k

    def fit(self, X, Y):
        self.X_tr = X
        self.Y_tr = Y

    def predict(self, X):
        Y_pred = [self._predict(x) for x in X]
        return np.array(Y_pred)

    def _predict(self, x):
        rastojanja = [rastojanje(x, x_tr) for x_tr in self.X_tr]
        ind = np.argsort(rastojanja)[:self.k]#sortirace indexe rastojanja prvih k suseda
        teme = [self.Y_tr[i] for i in ind]
        najcesci_slucaj = Counter(teme).most_common(1)#(1) broj najcescih suseda
        return najcesci_slucaj[0][0]# [(a, b),(),()..] a - cega ima navise od k najblizih, b - koliko

if __name__ == '__main__':
    
    from sklearn.model_selection import train_test_split
    from vektori_teme import podaci, tema#lepavina sa 12 tema (svaki deseti tekst uziman)
    
    vektori, teme = podaci()

    def uspesnost(Y_ts, Y_pred):
        uspesnost = np.sum(Y_ts == Y_pred) / len(Y_ts)
        return uspesnost

    X_tr, X_ts, Y_tr, Y_ts = train_test_split(vektori, teme, test_size = 0.2, random_state = 1)
    k = 3
    clf = KNN(k=k)
    clf.fit(X_tr, Y_tr)
    predvidjeno = clf.predict(X_ts)
    print('KNN uspesnost', int(round(uspesnost(Y_ts, predvidjeno), 2)*100), '%')
    
    
