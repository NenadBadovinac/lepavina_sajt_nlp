#from pandas import read_csv
import pandas as pd
from pandas.plotting import scatter_matrix
from matplotlib import pyplot
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

#url = pd.read_excel (r'iris3.xls')


url = "iris3.xls"
names = ['teoloski', 'duhovni', 'svetovni', 'naucni', 'kategorija']
#dataset = read_csv(url, names=names)
dataset = pd.read_excel(url, names=names)
print(dataset.head(20))

#Opis stupaca
print(dataset.describe())

# Distribucija klase kao poslednjeg atributa
print(dataset.groupby('kategorija').size())

# Multivarijantan analiza. Obratite pažnju na dijagonalno grupiranje nekih parova atributa. 
# To sugerira visoku korelaciju i predvidljiv odnos.
scatter_matrix(dataset)
pyplot.show()


# Moramo znati da je model koji smo stvorili dobar. 
# Kasnije ćemo stat.metodama proceniti tačnost modela. 
# Učitani skup podataka podijelit ćemo na dva dijela, od kojih ćemo 80% Trenirati, 
# procijeniti i odabrati među našim modelima. 
# 20% ćemo zadržati kao skup podataka za Testiranje i provjeru valjanosti.
# sada imamo X_Y train za Treniranje (80%),  X_Y za Testiranje (20%).
# Kad kažete array[:,0:4] to znači da se uzima prve 4 kolone našeg niza. 
# Kad kažete array[:,4] to znači da se uzima samo 5-ta kolon našeg niza. 
array = dataset.values
X = array[:,0:4]
y = array[:,4]
X_train, X_testiranje, Y_train, Y_testiranje = train_test_split(X, y, test_size=0.10, random_state=1)

print ("test", type(X_train))
#Izrada modela 
#Sada imamo 6 modela i procjene točnosti za svaki. 
#Moramo usporediti modele jedni s drugima i odabrati najtočnije.
#Izvodeći gornji primjer, dobivamo sljedeće neobrađene rezultate:

models = []
models.append(('LR', LogisticRegression(solver='liblinear', multi_class='ovr')))
#models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC(gamma='auto')))
# evaluate each model in turn
results = []
names = []
for name, model in models:
	kfold = StratifiedKFold(n_splits=7, random_state=1, shuffle=True)
	cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring='accuracy')
	results.append(cv_results)
	names.append(name)
	print('%s: %f (%f)' % (name, cv_results.mean(), cv_results.std()))


# Compare Algorithms
pyplot.boxplot(results, labels=names)
pyplot.title('Algorithm Comparison')
pyplot.show()



#PREDVIĐANJE
#Moramo odabrati algoritam koji ćemo koristiti za predviđanje.
#Rezultati u prethodnom odjeljku sugeriraju da je SVM možda bio najtočniji model. Ovaj model koristit ćemo kao konačni model.
#Sada želimo dobiti ideju o točnosti modela na našem skupu provjere valjanosti.
# Make predictions on testiranje dataset

model = SVC(gamma='auto')
model.fit(X_train, Y_train)
predictions = model.predict(X_testiranje)

# Evaluate predictions
#Predviđanja možemo procijeniti uspoređujući ih s očekivanim rezultatima 
#u skupu provjere valjanosti, zatim izračunati točnost klasifikacije, 
#kao i matricu zabune i izvješće o klasifikaciji.
#Možemo vidjeti da je točnost 0,966 ili oko 96% na skupu podataka o zadržavanju.
#Matrica zbrke daje naznaku učinjenih pogrešaka.
print("Na kraju, izvješće o klasifikaciji pruža raščlambu svake klase po preciznosti, opozivu, f1-bodu i podršci koja pokazuje izvrsne rezultate (ako je skup podataka za provjeru valjanosti bio mali)")

print(accuracy_score(Y_testiranje, predictions))
print(confusion_matrix(Y_testiranje, predictions))
print(classification_report(Y_testiranje, predictions))
