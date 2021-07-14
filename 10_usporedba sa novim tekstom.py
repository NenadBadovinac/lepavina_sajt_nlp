import pickle


with open('database\SVM_TfIDF_klasifikator_svi_postovi.pkl','rb') as f:
    klasifikator=pickle.load(f)


with open('database\TfIDF_testsize_10_svi_postovi.pkl','rb') as f:
    CV=pickle.load(f)
    
while True:
    k = input('\nUNESITE TEKST\n>>')
    if k.lower() != 'stop':
        l=[]
        m=[]
        l.append(k)
        m=CV.transform(l)
        predvidjeno = klasifikator.predict(m)
        print('\nTema je: {}'.format(predvidjeno[0]))
    else:
        break