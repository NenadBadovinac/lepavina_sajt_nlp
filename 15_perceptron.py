#PERCEPTRON
#neka je prostor 2D
#kod se odnosi na BINARNU KVALIFIKACIJU (0,1)
#u dvodimenzionalnom prostoru postoji n tacaka koje treba razgraniciti linijom
#neka je trenutna linija razgranicenja 2x + 4y - 8 = 0 (y = -1/2x + 2)
#neka postoji tacka sa koordinatama (3,1) (za x = 3, mora biti y = 1/2 da bi bila na liniji)
#tacka je iznad linije
#koeficijenti moraju biti smanjeni da bi jednacina prave sa vrednostima te tacke dala nulu
#princip: odgovarajuci koeficijenti se umanjuju za odgovarajucu koordinatu tacke
#(2-3)x + (4-1)y -(8-1) = 0 (y = 1/3x + 3)
#pomerili smo pravu navise i sada je ona rastuca
#uvodimo learning_rate (npr 0.01) da ne bi smo naglo otisli navise
#u trenutku kada vrednost jednacine za tu tacku bude manja od nule, tacka se nalazi ispod krive
#prestajemo da podizemo pravu


import numpy as np


class Perceptron:
    def __init__(self, learning_rate=0.01, n_iters=1000):
        self.lr = learning_rate
        self.n_iters = n_iters
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        n_samples, n_features = X.shape
        #u nasem slucaju [0,0]
        self.weights = np.zeros(n_features)
        #konstanta prave
        self.bias = 0

        for _ in range(self.n_iters):
            
            #za svaku tacku
            for ind, x_i in enumerate(X):
                #neka vrednost koja je veca ili manja od nule
                #ako je veca od nule, tacka je iznad linije i obrnuto
                linear_output = np.dot(x_i, self.weights) + self.bias
                #ako je vrednost veca od nule pripisujemo joj 1, u suprotnom 0
                y_predicted = self._unit_step_func(linear_output)
                #ako je tacka iznad linije, a treba da je ispod, update je lr*(-1)
                #ako je tacka ispod linije, a treba da je iznad, update je lr*1
                #ako je tacka tamo gde treba, update je 0
                update = self.lr * (y[ind] - y_predicted)
                #tezine se uvecavaju ili umanjuju po principu objasnjenom gore
                self.weights += update * x_i
                #ako je potrebno (ako tacka nije gde treba) bias se uvecava ili smanjuje za 1
                self.bias += update

    def predict(self, X):
        linear_output = np.dot(X, self.weights) + self.bias
        y_predicted = self._unit_step_func(linear_output)
        return y_predicted

    def _unit_step_func(self, x):
        #vrati np listu (tamo gde je x>=0, vrati 1, a u suprotnom 0)
        return np.where(x >= 0, 1, 0)


if __name__ == "__main__":
    from sklearn.model_selection import train_test_split
    from sklearn import datasets

    def accuracy(y_true, y_pred):
        accuracy = np.sum(y_true == y_pred) / len(y_true)
        return accuracy

    X, y = datasets.make_blobs(
        n_samples=150, n_features=2, centers=2, cluster_std=1.05, random_state=2)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=123)

    p = Perceptron(learning_rate=0.01, n_iters=1000)
    p.fit(X_train, y_train)
    predictions = p.predict(X_test)

    print("Perceptron classification accuracy", accuracy(y_test, predictions))
