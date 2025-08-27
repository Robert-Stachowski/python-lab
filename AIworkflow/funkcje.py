# FUNKCJE UŻYTKOWNIKA

def przywitaj_sie():
    print("Hello!")

przywitaj_sie()
print("----------------------------")


def przedstaw_sie(a,b):
    return f"Cześć {a} , masz {b} lata?!"

x = przedstaw_sie("Robert", 43)
print(x)
print("----------------------------")


def pole_kwadratu(a):
    return a*a

x = pole_kwadratu(5)
print(x)
print("----------------------------")


def czy_parzysta(liczba):
    return liczba % 2==0

liczba = int(input("Podaj liczbę: "))
if czy_parzysta(liczba):
    print("Parzysta")
else:
    print("Nieparzysta")
print("----------------------------")





# LAMBDA argumenty: wyrażenie




kwadrat = lambda x: x**2
print(kwadrat(4))
print("----------------------------")

# Funkcja anonimowa (lambda) – szybki sposób na prostą funkcję w jednej linijce.
# Składnia: lambda argumenty: wyrażenie
# Tworzymy funkcję, która zwraca kwadrat liczby.
# Zmienna 'kwadrat' działa jak nazwa funkcji.
# Wywołanie: kwadrat(4) → wstawia 4 w miejsce x → zwraca 4**2 = 16





# LAMBDA + Funkcje wbudowane map() filter() sorted() reduce() any() all() zip()





# map() - przekształcanie elementów
# map(funkcja, kolekcja) - sortuje funkcję do każdego elementu
# map() działa na każdym obiekcie iterowalnym
# Zwraca iterator, więc często zmieniamy na listę, tuple, set w zależności od potrzeb.

liczby = [1,2,3,4,5]
kwadrat = list(map(lambda x: x**2, liczby))             # List
print(kwadrat)
print("----------------------------")
# map() + lambda – szybkie przekształcanie elementów listy.
# 1. Mamy listę liczb: [1, 2, 3, 4, 5].
# 2. Funkcja map() stosuje podaną funkcję (tu: lambda x: x**2) do każdego elementu listy.
#    - lambda x: x**2 oznacza: weź liczbę x i zwróć x do kwadratu.
# 3. map() zwraca specjalny obiekt (iterator), więc zamieniamy go na listę przy pomocy list().
# 4. Wynik to nowa lista kwadratów: [1, 4, 9, 16, 25].

liczby = (1, 2, 3, 4)
kwadraty = tuple(map(lambda x: x**2, liczby))           # Tuple
print(kwadraty)  # (1, 4, 9, 16)
print("----------------------------")


liczby = {1, 2, 3, 4}
kwadraty = set(map(lambda x: x**2, liczby))             # Set
print(kwadraty)  # {16, 1, 4, 9}
print("----------------------------")


napis = "Python"
duze = list(map(lambda x: x.upper(), napis))            # String
print(duze)  # ['P', 'Y', 'T', 'H', 'O', 'N']
print("----------------------------")


slownik = {"a": 1, "b": 2, "c": 3}
klucze_duze = list(map(lambda x: x.upper(), slownik))   # Dict
print(klucze_duze)  # ['A', 'B', 'C']
print("----------------------------")






# filter() - filtrowanie danych, na dowolnym iterowalnym obiekcie (lista,krotka,zbiór,string)
# filter() zawsze zwraca iterator (coś, po czym można iterować raz), więc często zamieniasz go na listę, 
# tuple, set w zależności od potrzeb.
# filter(funkcja,kolekcja) - zwraca tylko elementy dla których funkcja da True!

liczby = [1,2,3,4,5,6]
parzyste = list(filter(lambda x: x % 2 ==0, liczby))
print(parzyste)
print("----------------------------")
# filter() + lambda – szybkie filtrowanie elementów listy.
# 1. Mamy listę liczb: [1, 2, 3, 4, 5, 6].
# 2. Funkcja filter() wybiera tylko te elementy, dla których funkcja zwróci True.
#    - lambda x: x % 2 == 0 sprawdza, czy liczba jest parzysta.
# 3. filter() zwraca obiekt typu filter (iterator), czyli "strumień danych".
#    - Aby zobaczyć wynik jako zwykłą listę, zamieniamy na listę funkcją list().

liczby = (1, 2, 3, 4)
wynik = tuple(filter(lambda x: x % 2 == 0, liczby))
print(wynik)  # (2, 4)
print("----------------------------")


slowo = "Python"
samogloski = list(filter(lambda x: x.lower() in "aeiouy", slowo))
print(samogloski)  # ['o']
print("----------------------------")


liczby = {1, 2, 3, 4}
wynik = set(filter(lambda x: x > 2, liczby))
print(wynik)  # {3, 4}
print("----------------------------")






