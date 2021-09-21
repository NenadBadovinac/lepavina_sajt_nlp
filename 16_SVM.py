# neka prava ima formulu <w><x> = b, gde je <w> vektor normalan na pravu a <x> vektor koji se nalazi na pravoj
# proizvod ova dva vektora je skalar koji uvek ima istu vrednost - b (projekcija na normalu prave je ista za sve tacke linije)
# rastojanje linije od koordinatnog pocetka = b/||w|| gde je ||w|| duzina vektora w 
# zelimo takvu pravu gde za sve + uzorke vazi <w><x> > b, a za sve - uzorke <w><x> < b - uslov za klasifikaciju
# takvih pravi ima puno i po razlicitim dimenzijama
# najbolja prava je ona gde je rastojanje izmedju + i - uzoraka najsire - 'widest street approach'
# ideja je da se otkriju <w> i b koji najbolje zadovojavaju 'widest street approach'
# sada zelimo takvu pravu gde za sve + uzorke vazi <w><x> >= b + 1, a za sve - uzorke <w><x> <= b - 1
# za + -> <w><x> - b >= 1, za - -> <w><x> - b <= -1
# y odredjuje klasu kojoj pripada svaka tacka pripisujuci +1 ili -1
# sledi y(<w><x> - b) >= 1 za sve tacke
# koliko je siroka ulica?
# neka dve tacke pripadaju ivicama margine <w><x+> = b + 1, <w><x-> = b - 1
# (<x+>-<x->)(<w>/||w||) predstavlja sirinu ulice
# sirina ulice = 2/||w||
# zelimo da maximizujemo 2/||w|| ~ min ||w|| ~ min 1/2||w||^2 (zgodno je matematicki to postaviti ovako)
# L = lambda*1/2||w||^2 + 1/n*sum[max(0, 1 - y(<w><x> - b))]
# zelimo da suma odstupanja svih tacaka od margina bude maximalna, ali ujedno i da ulica bude najsira moguca
# treba nam minimum funkcije L
# kada y(<w><xi> - b) > 1 (tacka se ne nalazi u margini), L(i) = lambda*||w||^2  
# dL(i)/d(<w>) = 2*lambda*<w>
# kada je ovo slucaj, ||w|| treba smanjiti, tj prosiriti marginu <w> -= learning_rate*(2*lambda*<w>)
# (2*lambda*<w>) je strmost koja diktira koliko brzo zelimo da idemo
# kada y(<w><xi> - b) < 1 (tacka se nalazi u margini), L(i) = lambda*||w||^2 + (1 - y(<w><xi> - b))
# dL(i)/d(<w>) = 2*lambda*<w> - y<xi> (ovo pomera <w> ka <xi> i daje tacki mogucnost da izadje iz margine)



import numpy as np

class SVM:
    def __init__(self, learning_rate=0.001, lambda_param=0.01, n_iters=100):
        self.lr = learning_rate
        self.lambda_param = lambda_param
        self.n_iters = n_iters
        self.w = None
        self.b = None

    def fit(self, X, y):
        n_samples, n_features = X.shape

        self.w = np.zeros(n_features)
        self.b = 0

        for _ in range(self.n_iters):
            for idx, x_i in enumerate(X):
                condition = y[idx] * (np.dot(x_i, self.w) - self.b) >= 1
                if condition:
                    self.w -= self.lr * (2 * self.lambda_param * self.w)
                else:
                    # tacka na pogresnoj strani prave:
                    # kada je y = +1, koordinate <w> se uvecavaju sto spusta i rotira marginu tako da tacka dodje ispod
                    # kada je y = -1, sve obrnuto  
                    self.w -= self.lr * (2 * self.lambda_param * self.w - np.dot(x_i, y[idx]))
                    # ako je y = +1, odsecak se umanjuje tako da margina dodje ispod nje
                    # ako je y = -1, odsecak se uvecava tako da margina dodje iznad nje
                    self.b -= self.lr * y[idx]
                    # u svakom slucaju, ovo rotira pravu, pomera odsecak, siri marginu itd..
    def predict(self, X):
        approx = np.dot(X, self.w) - self.b
        return np.sign(approx)


if __name__ == "__main__":
    from sklearn import datasets
    import matplotlib.pyplot as plt

    X, y = datasets.make_blobs(n_samples=50, n_features=2, centers=2, cluster_std=1.05, random_state=40)

    y = np.where(y == 0, -1, 1)

    clf = SVM()
    clf.fit(X, y)

    print(clf.w, clf.b)

    #predvidjamo
    X_ts = np.array([[-3,4],[3,4],[5,6]])
    r = clf.predict(X_ts)
    print(r)


    def visualize_svm():
        def get_hyperplane_value(x, w, b, offset):
            return (-w[0] * x + b + offset) / w[1]

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        plt.scatter(X[:, 0], X[:, 1], marker="o", c=y)

        x0_1 = np.amin(X[:, 0])
        x0_2 = np.amax(X[:, 0])

        x1_1 = get_hyperplane_value(x0_1, clf.w, clf.b, 0)
        x1_2 = get_hyperplane_value(x0_2, clf.w, clf.b, 0)

        x1_1_m = get_hyperplane_value(x0_1, clf.w, clf.b, -1)
        x1_2_m = get_hyperplane_value(x0_2, clf.w, clf.b, -1)

        x1_1_p = get_hyperplane_value(x0_1, clf.w, clf.b, 1)
        x1_2_p = get_hyperplane_value(x0_2, clf.w, clf.b, 1)

        ax.plot([x0_1, x0_2], [x1_1, x1_2], "y--")
        ax.plot([x0_1, x0_2], [x1_1_m, x1_2_m], "k")
        ax.plot([x0_1, x0_2], [x1_1_p, x1_2_p], "k")

        x1_min = np.amin(X[:, 1])
        x1_max = np.amax(X[:, 1])
        ax.set_ylim([x1_min - 3, x1_max + 3])

        plt.show()

    visualize_svm()