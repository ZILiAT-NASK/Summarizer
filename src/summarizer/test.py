from summarizer import Summarizer

sum = Summarizer()

dane='''Dokonując w tym miejscu reasumpcji przedstawionej argumentacji, należy zauważyć, co następuje.
1. W analizowanej sprawie nie znajdują zastosowania przepisy ustawy - Ordynacja podatkowa dotyczące przedawnienia.
Zagadnienie związane z możliwością dochodzenia opiat wynikających z decyzji środowiskowych w określonym czasie, zostało uregulowane w przepisie art. 56b ust. 2 ustawy z dnia 24 października 1974 r.
- Prawo wodne.
Jednocześnie w niniejszej sprawie należ uwzględnić wynikający z przepisu art. 15 Rozporządzenia Rady nr 659/1999 1 O - letni termin przedawnienia przewidziany na dochodzenie zwrotu nielegalnej pomocy publicznej.
2. Ustalenie podmiotu zobowiązanego do zwrotu pomocy publicznej oraz właściwego trybu jej dochodzenia wymaga przesądzenia do jakiej kategorii pomocy publicznej należy zaliczyć należności Wojewody Śląskiego wynikające z decyzji środowiskowych .
Kwestia ta nie wynika jednoznacznie, ani z treści decyzji KE, ani z pozostałych, przedstawionych Prokuratorii Generalnej dokumentów.
W konsekwencji w niniejszej opinii wskazano dwa warianty dotyczące odzyskania pomocy publicznej oraz zasadnicze ryzyka prawne związane z egzekucją pomocy publicznej od podmiotu niewłaściwego.
Z uwagi jednak na znaczenie ww.
zagadnienia dla niniejszej sprawy, celowym wydaje się podjęcie działań związanych z ustaleniem do jakiej kategorii pomocy publicznej została zakwalifikowana wierzytelność Wojewody Śląskiego.
W tym celu, zasadnym wydaje się sięgnięcie do wszelkich materiałów związanych z formalną procedurą dochodzenia prowadzoną przez Komisję Europejską, w trakcie której strona polska przedstawiała wyjaśnienia związane ze stanem zadłużenia 3. Gdyby okazało się, że pomoc udzieloną przez Wojewodę Śląskiego należy zakwalifikować do kategorii pomocy, o której mowa w art. 3 ust. 1, podmiotami zobowiązanymi do zwrotu byłyby spółki zależne: ffs1~ przymusowe zaś ściągnięcie kwot zakwestionowanej pomocy powinno nastąpić w trybie przepisów ustawy o postępowaniu egzekucyjnym w administracji.
4. Jeżeli pomoc udzielona przez Wojewodę Śląskiego mieści się w kategorii pomocy, o której mowa w art. 3 ust. 2, to podmiotem zobowiązanym do jej zwrotu byłaby spółka dochodzenia - zgłoszenie wierzytelności w postępowaniu upadłościowym.
a trybem jej 5. Odzyskanie pomocy od niewłaściwego podmiotu może się wiązać z wszczęciem przez Komisję Europejską (lub inne zainteresowane państwo członkowskie) postępowania przed Trybunałem Sprawiedliwości Wspólnot Europejskich na podstawie art. 88 ust. 2 Traktatu ustanawiającego Wspólnotę Europejską.
Nie można wykluczyć w takiej sytuacji odpowiedzialności odszkodowawczej Skarbu Państwa na płaszczyźnie krajowej.
Natomiast w odniesieniu do przedstawionych we wniosku o wydanie opinii wątpliwości związanych z wystawieniem tytułu wykonawczego, należy zauważyć, że przedstawione uwagi nie naświetlają precyzyjnie zagadnienia, które by wymagało wyjaśnienia przez Prokuratorię Generalną Skarbu Państwa.
Należy odnotować, że w sytuacji, gdyby Wojewoda Śląski był zobowiązany do odzyskania pomocy od to tytuł wykonawczy powinien być wystawiony na ww. podmioty.
Chociaż decyzja ustalająca należności środowiskowe była wystawiona na inny podmiot, to należałoby przyjąć, że na podstawie decyzji Komisji Europejskiej, która jest wiążąca dla wszystkich organów Państwa (por. wyrok w sprawie 14 września 1994 r., nr C-42/93) oraz art. 25 ust. 1 ustawy o postępowaniu w sprawach dotyczących pomocy publicznej, zobowiązanymi do zwrotu tych należności są ww.
spółki zależne.
Zgodnie z ustawą z dnia 17 czerwca 1966 r. o postępowaniu egzekucyjnym w administracji (Dz. U z 2005 r., nr 229, poz. 1954), uprawnionym do żądania wykonania w drodze egzekucji administracyjnej jest dla obowiązków wynikających z orzeczeń sądów lub innych organów albo bezpośrednio z przepisów prawa - organ lub instytucja bezpośrednio zainteresowana w wykonaniu przez zobowiązanego obowiązku albo powołana do czuwania nad wykonaniem obowiązku, a w przypadku braku takiej jednostki lub bezczynności - podmiot, na którego rzecz wydane zostało orzeczenie lub którego interesy prawne zostały naruszone w wyniku niewykonania obowiązku (art. 5 § 1 pkt 2 ww. ustawy).
Natomiast właściwość organów egzekucyjnych określa rozdział 2 ustawy o postępowaniu egzekucyjnym w administracji.
Zgodnie z przepisami tej ustawy Wojewoda występuje jako organ egzekucyjny jedynie w odniesieniu do egzekucji administracyjnej obowiązków o charakterze niepieniężnym (por. art. 20 § 1 pkt 1 ww. ustawy) , co nie dotyczy analizowanego przypadku.
Z uwagi na brak szczególnych regulacji w tym zakresie, wydaje się, że organem egzekucyjnym byłby - zgodnie z ogólną kompetencją - Naczelnik właściwego urzędu skarbowego (art. 19 § 1 ustawy o postępowaniu egzekucyjnym w administracji).
Należy jednak odnotować, że stosownie do art. 26 § 1 ustawy o postępowaniu egzekucyjnym w administracji, organ egzekucyjny wszczyna egzekucję administracyjną na wniosek wierzyciela i na podstawie wystawionego przez niego tytułu wykonawczego, sporządzonego wg ustalonego wzoru.
W konsekwencji, stosownie do dyspozycji ww.
przepisu, wydaję się, że tytuł wykonawczy powinien zostać wystawiony przez Wojewodę Śląskiego.'''

# print(len(dane))
print(sum.summarize(dane, 1500, 'chars', alg_type='lemmas')['summary'])
print('-----------------')
print(sum.summarize(dane, 1500, 'chars', alg_type='words')['summary'])
print('-----------------')
print(sum.summarize(dane, 1500, 'chars', alg_type='coreferences')['summary'])