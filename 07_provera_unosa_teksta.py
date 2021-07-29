import string


tekst = '''
Ovdje ću na početku odgovoriti tekstom episkopa Nikodima Milaša gdje govori o nastanku ove episkopske titule.

U svetome Pismu mi ne nalazimo izričnoga mjesta, iz koga bi se videlo, da su horepiskopi u apostolskoj crkvi postojali. Okolnosti crkve hristjanske ta dašnjeg doba dopuštaju nam ipak predpolagati, da su horepiskopi i u ono još doba bili. Crkva je tada bila okružena sa sviju strana neznabožcima, koje je trebalo usiljenim sredstvima prosvjećivati evangelskom naukom. Nije ona slobodna bila ni od različitih jeretika, koji, da uspješnije djeluju u rasprostiranju svojih lažnih nauka, staraxu se da postavljaju jednomišljenike svoje u svima i najmanjim mjestima za episkope i prezvitere.

Protivu jednih i drugih, crkva je morala usiliti svoju obranu, da pobjedu pravoslavlju i vjernima izvojuje :ona je postavljala u svakome i najmanjem mjestu pravoslavne episkope, preporučujući nam, da narod uzdržuju u čistoj nauci, da pravoslavni klir hrabre u borbi s neprijateljima crkve i da svugdje dostojne svešteno i crkvenoslužitelje postavljaju. Episkopi tih manjih mjesta ili sela nazivali su se obćim imenom selskih episkopa, da se razlikuju od onih, koji su u gradovima bili, od gradskiя episkopa. Vlast ovih u svome mjestu bila je jednaka vlasti gradskih episkopa u svojim gradovima ; odnošaj pak između njih bio je od prilike onaj koji je poslje ustanovljen između epi kopa i prvog episkopa , — ili, služeći se izrazima kanoničkima, vlast horepiskopa u svome okrugu bila je jednaka vlasti gradskog episkopa u svojoj eparhiji, odnošaj između njih bio je priblizno onaj, što je postojao između eparhijalnih episkopa i episkopa mitropole .[4]

Prvi izričniji spomen o horepiskopima nalazimo u І poslanici Klimenta Rimskog Koriićanima : Praedicantes per regiones ac urbes , primitias earum, spiritu cum probassent, in episcopos el diaconos eorum qui credturi erant, constituerunt . Evsevije u svojoj crkvenoj istoriji, govoreći o Antiohijskome saboru protivu Pavla Samosatskog, kaže : Istim načinom On je dopuštao sebi propovjedati narodu i episkopima obližnjih gradova i sela, i prezviterima, koji mu laskaxy“ . U opaskama na Evsevijevu istoriju ruskog izdanja, čitamo na spomenute rječi: „ Treba razumjevati shogeriscopos , ili selske episkope, koji su mitropoliji podvlastni bili“ . Podobno ovome govori i latinski izdavač istorije Evsevija : Chorepiscopos intelligere vіdelur. Eosenim distinguit epistols ab Episcopis urbium „. Uzimajući u obzir doba kad je Kliment rimski živio i vreme kad je držan sabor u Antiohiji protivu Pavla Samosatskog, o kome Evsevije spominje, mora se smatrati pogrješnom misao Ind. Thomassin-a, koji tvrdi : Chorepiscopos tria priora saecula habuisse nollos, eosque noviter institutos esse , quia non fuisse bis leinporibus in agris ecclesias constitutas. Ne može se ovo dopustiti ni s’ pogleda na ime jer episkopi obližnih sela , o kojima spominje Evsevije, svakako sliorepiscopi ili Episcopi rurales seu villani moraju biti. Ne može se ustvrditi ni to, da su tek sabori IV vjeka horepiskope ustanovili, jer način, kojim se u svojim pravilima ti sabori izražavaju, pokazuje, da su horepiskopi u to doba bili dobro poznati i njihov djelokrug više ili manje ocpnjen. Ustanova horepiskopa dakle odnosi se svakako u najstarijem dobu crkve hristjanske, ka vremenima apostola , ili bar muževa apostolskih. Sabori koji o horepiskopima govore, jasno nam kazuju, da horepiskopi ne samo što su se razlikovali od prezvitera, nego su pravim, samo zavisnim ograničenom vlašću, episkopima smatrani bili.[5]
'''

def filtriranje(tekst):
    
    sadrzaj = list(map(lambda a: a.strip('\u201a'), tekst.split()))
    sadrzaj = list(map(lambda a: a.strip('\u201e'), sadrzaj))
    sadrzaj = list(map(lambda a: a.strip('\u201c'), sadrzaj))
    sadrzaj = list(map(lambda a: a.strip('\u201d'), sadrzaj))
    sadrzaj = list(map(lambda a: a.strip('\u2026'), sadrzaj))
    sadrzaj = list(map(lambda a: a.strip(string.punctuation + string.whitespace), sadrzaj))

    return sadrzaj

print(filtriranje(tekst))



