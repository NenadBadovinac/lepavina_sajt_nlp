#bayes - kolika je verovatnoca da nesto sa odredjenom karakteristikom pripada odredjenoj kategoriji
#P(Yi|Xi) = P(Yi)P(Xi|Yi)/P(Xi)
#Yi - jabuka ; Xi - crvena boja
#P(Xi) - verovatnoca da voce bude crveno
#P(Yi)P(Yi) - verovatnoca da voce bude crvena jabuka
#P(Yi|Xi) - verovatnoca da je crveno voce jabuka
#kada poredimo verovatnoce da voce bude crveno trazimo voce koje ima maximalnu vrednost
#P(Xi) je jednako za svako voce, pa taj faktor ne moramo da racunamo
#naive - predpostavlja se da ako ima vise karakteristika, one ne zavise jedne od drugih
#P(X1,...,Xn|Yi) = P(X1|Yi)...P(Xn|Yi) - naive
#P(Yi|X1,...,Xn) ~ P(Yi)P(X1|Yi)...P(Xn|Yi)
#za svaku kategoriju racunamo P(Yi)
#racunamo i udeo onih koji imaju datu karakteristiku (Xi) u okviru date kategorije (Yi)
#za odredjenu kombinaciju X trazimo kategoriju sa maksimalnom verovatnocom

#problem - imamo tekst sa odredjenim recnikom X
#uzorak sa odredjenom kategorijom tekstova je mali (npr 1 tekst)
#uzorak sa drugom kategorijom tekstova je veliki (npr 1000)
#ako primenimo algoritam odozgo P(Y1) << P(Y2) pa su i takve kvalifikacije

#multinomial naive bayas - primena na tekst
#verovatnoca da se ta rec nalazi u kategoriji 
#P(Xi|Yi) ~ N(Yi|Xi) + a / N(Yi) + an
#N(Yi|Xi) - ukupan broj ponavljanja date reci (Xi) u kategoriji (Yi)
#N(Yi) - ukupan broj svih reci u kategoriji (Yi)
#0 < a < 1 - podesiti na neku vrednost jer ako reci uopste nema u datoj kategoriji P ce biti nula
#n - broj reci
#na ovaj nacin smo dobili verovatnocu da se rec pojavi u tekstu date kategorije P(Xi|Yi)
#P(Yi|X1,...,Xn) ~ P(Yi)P(X1|Yi)^f1...P(Xn|Yi)^fn - f su frekvencije pojavljivanja reci u ispitivanom tekstu
#P(Xi|Yi) su male vrednosti, a mnozenjem verovatnoca za svaku karakteristiku vrlo lako dolazi do underfloa
#underflow - toliko male vrednosti da komp ne moze da ih racuna
#P(Yi|X1,...,Xn) ~ log(P(Yi)) + f1*log(P(X1|Yi)) + ... + fn*log(P(Xn|Yi))
#logaritam od i (0 < i < 1) je negativan
#na kraju, moze se primeniti idf na frekvenciju
#P(Yi|X1,...,Xn) ~ log(P(Yi)) + log(1 + f1)*log(P(X1|Yi)) + ... + log(1 + fn)*log(P(Xn|Yi))

# 1 pretvoriti sve pripremljene tekstove u vektore
# 2 odrediti P(Yi) - koliki je udeo kategorija
# 3 napraviti matricu (broj reci x broj kategorija) sa log(P(Xi|Yi))
# 4 naci P(Yi|X1,...,Xn) svakog teksta za svaku kategoriju i pripisati kategoriju maximalnoj vrednosti


import numpy as np


class NB:
    
    def fit(self, X, Y):

        a = 0.001

        n_red, n_atr = X.shape
        self._klase, counts = np.unique(Y, return_counts = True)
        self._klase_P = counts/n_red
        n_klase = len(self._klase)
        
        self._N = np.zeros((n_klase, n_atr))    

        for i, tema in enumerate(self._klase):
            m = X[Y == tema]
            Z = m.sum(axis = 0)
            self._N[i] = np.log2((Z + a)/(Z.sum() + n_atr*a))


    def predict(self, X):
        Y_pred = [self._predict(x) for x in X]
        return np.array(Y_pred)

    
    def _predict(self, x):            
        x = np.log2(1 + x)
        scores = np.sum(x * self._N, axis = 1) + np.log2(self._klase_P)
        return self._klase[np.argmax(scores)]
        


if __name__ == '__main__':
    
    from sklearn.model_selection import train_test_split
    from vektori_teme_count import podaci, tema #lepavina sa 12 tema (svaki deseti tekst uziman)
    
    vektori, teme = podaci()

    def uspesnost(Y_ts, Y_pred):
        uspesnost = np.sum(Y_ts == Y_pred) / len(Y_ts)
        return uspesnost

    X_tr, X_ts, Y_tr, Y_ts = train_test_split(vektori, teme, test_size = 0.2, random_state = 1)

    nb = NB()
    nb.fit(X_tr, Y_tr)
    Y_pred = nb.predict(X_ts)
    
    print('NB uspesnost', int(round(uspesnost(Y_ts, Y_pred), 2)*100), '%')





