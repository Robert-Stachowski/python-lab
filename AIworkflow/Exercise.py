lista = []                  # pustą listę
lista.append(1)             # dodaj 1 na koniec -> [1]
lista.extend([2, 3])        # dodaj kilka elementów -> [1, 2, 3]
lista.insert(1, 5)          # wstaw 5 na indeks 1 -> [1, 5, 2, 3]
lista.remove(5)             # usuń pierwsze wystąpienie 5 -> [1, 2, 3]
lista.pop()                 # usuń i zwróć ostatni (3) -> [1, 2]
del lista[0]                # usuń element na indeksie 0 -> [2]
lista.clear()               # usuń wszystko -> []


zbior = set()               # pusty zbiór
zbior.add(5)                # dodaj 5 -> {5}
zbior.update([6, 7])        # dodaj kilka elementów -> {5, 6, 7}
zbior.discard(8)            # usuń 8, jeśli istnieje (bez błędu)
zbior.remove(5)             # usuń 5 (błąd, jeśli nie ma)
zbior.pop()                 # usuń i zwróć losowy element
zbior.clear()               # usuń wszystko -> set()


slownik = {}                # pusty słownik
slownik['a'] = 1            # dodaj klucz 'a' -> {'a': 1}
slownik.update({'b': 2})    # dodaj/zmień kilka par -> {'a': 1, 'b': 2}
wartosc = slownik.pop('a')  # usuń 'a' i zwróć 1 -> {'b': 2}
del slownik['b']            # usuń klucz 'b' -> {}
slownik.clear()             # usuń wszystko -> {}


krotka = ()                 # pusta krotka
krotka = (1, 2)             # krotka z elementami
krotka = krotka + (3,)      # dodanie = nowa krotka (1, 2, 3)
# brak metod dodawania/usuwania – niemutowalna





# Exercise




num22 = [1,2,2,3,4,4,5]
uniqe_num22 = {x for x in num22} # Utworzenie unikalnego zbioru {set}
print(uniqe_num22)
print("-----------------------")




aa = { x for x in list(range(20)) if x % 2 == 0 }
print(aa)

x = set()
for i in range(20):
    if i % 2 == 0:
        x.add(i)

print(x)