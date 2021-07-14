data = {'marko': [45, 'dedarkovica1', (150, 'plav')],
        'nenad': [35, 'dedarkovica2', (190, 'crn')]}


print(data['marko'][2][0])

data['mihajlo'] = [45, 'dedarkovica1', (150, 'plav')]

print(data)

for kljuc, vrednosti in data.items():
    print(kljuc, vrednosti[2][0])