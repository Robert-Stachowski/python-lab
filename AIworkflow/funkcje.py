# FUNKCJE UŻYTKOWNIKA

def przywitaj_sie():
    print("Hello!")

przywitaj_sie()
print("----------------------------")


def przedstaw_sie(a,b):
    return f"Cześć {a}, masz {b} lata?!"

x = przedstaw_sie("Robert", 43)
print(x)
print("----------------------------")


def pole_kwadratu(a):
    return a*a

x = pole_kwadratu(5)
print(x)
print("----------------------------")


def czy_parzysta(liczba):
    return liczba % 2 == 0

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





# MAP() - przekształcanie elementów

# map(funkcja, kolekcja) - stosuje funkcję do każdego elementu
# map() działa na każdym obiekcie iterowalnym
# Zwraca iterator, więc często zmieniamy na listę, tuple, set w zależności od potrzeb.

liczby = [1,2,3,4,5]
kwadraty = list(map(lambda x: x**2, liczby))             # List
print(kwadraty)
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






# FILTER() - filtrowanie danych, na dowolnym iterowalnym obiekcie (lista,krotka,zbiór,string)

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
print(samogloski)  # ['y', 'o']
print("----------------------------")


liczby = {1, 2, 3, 4}
wynik = set(filter(lambda x: x > 2, liczby))
print(wynik)  # {3, 4}
print("----------------------------")





from functools import reduce

# REDUCE() – "redukuje" kolekcję do jednej wartości, krok po kroku. reduce(funkcja, kolekcja[, wartość_startowa])

# funkcja – musi przyjmować dwa argumenty (np. lambda a, b: a + b),
# kolekcja – lista, krotka, dowolny iterowalny obiekt,
# wartość_startowa (opcjonalna) – jeśli podasz, zaczyna od niej (jakby dodatkowy pierwszy element).

# Jak działa?
# - Przyjmuje funkcję z dwoma argumentami (tu: lambda a, b: a + b).
# - Bierze pierwsze dwa elementy listy i łączy je.
# - Wynik tego działania łączy z kolejnym elementem.
# - Powtarza aż do końca – na końcu zostaje jedna wartość.
# 
# Tutaj: sumujemy wszystkie liczby w liście.
liczby = [1, 2, 3, 4]
suma = reduce(lambda a, b: a + b, liczby)
print(suma)  # 10

# Start: lista [1, 2, 3, 4].
# reduce bierze pierwsze dwa elementy: 1 i 2 → 1 + 2 = 3.
# Wynik 3 łączy z kolejnym elementem 3 → 3 + 3 = 6.
# Wynik 6 łączy z ostatnim elementem 4 → 6 + 4 = 10.
# Zwraca 10.

liczby = [1, 2, 3, 4]
suma = reduce(lambda a, b: a + b, liczby, 10)               # Przykład z wartością startową
print(suma)  # 20 (bo zaczyna od 10 + 1 + 2 + 3 + 4)



max_val = reduce(lambda a, b: a if a > b else b, liczby)
print(max_val)
# Szukanie największej

iloczyn = reduce(lambda a, b: a * b, liczby)
print(iloczyn)
# Mnożenie wszystkich elementów






# any(), all(), zip() 





# --- any() ---

# any() zwraca True, jeśli CHOĆ JEDEN element kolekcji jest "prawdziwy" (nie 0, nie pusty, nie False).

# Przykład 1 – liczby:
liczby = [0, 0, 5, 0]
print(any(liczby))  # True (bo 5 jest różne od 0)

# Przykład 2 – warunek w liście:
print(any(x > 10 for x in [2, 15, 7]))  # True (15 > 10)

# Przykład 3 – napisy:
slowa = ["", "", "Python"]
print(any(slowa))  # True (bo "Python" to niepusty string)





# --- all() ---

# all() zwraca True, jeśli WSZYSTKIE elementy kolekcji są "prawdziwe".
# Jeśli chociaż jeden jest False/pusty/0 → wynik False.

# Przykład 1 – liczby:
liczby = [2, 4, 6]
print(all(x % 2 == 0 for x in liczby))  # True (wszystkie parzyste)

# Przykład 2 – boolowska lista:
print(all([True, True, True]))  # True (wszyscy mówią "tak")
print(all([True, False, True]))  # False (bo jest False)

# Przykład 3 – napisy:
slowa = ["Ala", "Ola", "Jan"]
print(all(slowa))  # True (żaden nie jest pusty)




# --- zip() ---

# zip() łączy elementy z kilku kolekcji w PARY (krotki).
# Zwraca iterator → zwykle zamieniamy na listę lub przechodzimy pętlą.

# Przykład 1 – dwie listy:
imiona = ["Ala", "Ola", "Jan"]
wiek = [25, 30, 40]
połączone = list(zip(imiona, wiek))
print(połączone)  # [('Ala', 25), ('Ola', 30), ('Jan', 40)]

# Przykład 2 – trzy listy:
miasta = ["Poznań", "Warszawa", "Kraków"]
pensje = [4000, 5000, 4500]
pakiety = list(zip(imiona, miasta, pensje))
print(pakiety)  # [('Ala', 'Poznań', 4000), ('Ola', 'Warszawa', 5000), ('Jan', 'Kraków', 4500)]

# Przykład 3 – przejście po parach w pętli:
for name, age in zip(imiona, wiek):
    print(f"{name} ma {age} lat.")
# Wynik:
# Ala ma 25 lat.
# Ola ma 30 lat.
# Jan ma 40 lat.





# ====================================






# --- len() ---


# len() zwraca liczbę elementów w kolekcji (lista, string, tuple, dict, set).
lista = [1, 2, 3, 4]
print(len(lista))  # 4

tekst = "Python"
print(len(tekst))  # 6 (liczba znaków)

slownik = {"a": 1, "b": 2}
print(len(slownik))  # 2 (liczba kluczy)


# --- sum() ---


# sum() dodaje wszystkie elementy iterowalnego obiektu (liczby).
# Można dodać wartość startową jako drugi argument.
liczby = [1, 2, 3, 4]
print(sum(liczby))  # 10

liczby_tuple = (1, 2, 3, 4)
print(sum(liczby_tuple, 10))  # 20 (zaczyna od 10)

# sum() z warunkiem (np. suma parzystych)
print(sum(x for x in range(10) if x % 2 == 0))  # 20


# --- max() ---


# max() zwraca największy element z kolekcji.
# Można użyć parametru key do zmiany kryterium.
liczby = [1, 7, 3, 9]
print(max(liczby))  # 9

zbior = {10, 2, 50, 23}
print(max(zbior))  # 50

slowa = ["kot", "hipopotam", "pies"]
print(max(slowa, key=len))  # "hipopotam" (najdłuższy wyraz)


# --- min() ---


# min() zwraca najmniejszy element.
# Tak samo można użyć key.
liczby = [1, 7, 3, 9]
print(min(liczby))  # 1

krotka = (100, 20, -5, 50)
print(min(krotka))  # -5

slowa = ["kot", "hipopotam", "pies"]
print(min(slowa, key=len))  # "kot" (najkrótszy wyraz)


# --- round() ---


# round() zaokrągla liczbę. 
# Jeśli podasz drugi argument, określa liczbę miejsc po przecinku.
print(round(3.75))        # 4 (do całkowitej)
print(round(3.14159, 2))  # 3.14 (dwa miejsca)
print(round(-2.718, 1))   # -2.7


# --- abs() ---


# abs() zwraca wartość bezwzględną (usuwa znak minus).
print(abs(5))     # 5
print(abs(-7))    # 7
print(abs(-3.14)) # 3.14


# --- sorted() ---


# sorted() zwraca NOWĄ listę z posortowanymi elementami.
# Można dodać reverse=True i key.
liczby = [5, 2, 9, 1]
print(sorted(liczby))                  # [1, 2, 5, 9]
print(sorted(liczby, reverse=True))    # [9, 5, 2, 1]
slowa = ["kot", "hipopotam", "pies"]
print(sorted(slowa, key=len))          # ['kot', 'pies', 'hipopotam']


# --- map() ---


# map() stosuje funkcję do każdego elementu kolekcji.
# Zwraca iterator → często zamieniamy na listę.
liczby = [1, 2, 3, 4, 5]
kwadraty = list(map(lambda x: x**2, liczby))
print(kwadraty)  # [1, 4, 9, 16, 25]

napis = "Python"
duze = list(map(lambda x: x.upper(), napis))
print(duze)  # ['P', 'Y', 'T', 'H', 'O', 'N']

slownik = {"a": 1, "b": 2, "c": 3}
klucze_duze = list(map(lambda x: x.upper(), slownik))
print(klucze_duze)  # ['A', 'B', 'C']


# --- filter() ---


# filter() wybiera elementy spełniające warunek.
# Zwraca iterator → zamieniamy na listę, tuple, set.
liczby = [1, 2, 3, 4, 5, 6]
parzyste = list(filter(lambda x: x % 2 == 0, liczby))
print(parzyste)  # [2, 4, 6]

napis = "Python"
samogloski = list(filter(lambda x: x.lower() in "aeiouy", napis))
print(samogloski)  # ['y', 'o']

slowa = ["", "pies", "", "kot"]
niepuste = list(filter(None, slowa))
print(niepuste)  # ['pies', 'kot']


# --- any() i all() ---


# any() – True jeśli CHOĆ JEDEN element jest truthy (np. nie 0, nie pusty)
# all() – True jeśli WSZYSTKIE elementy są truthy.
liczby = [0, 0, 5]
print(any(liczby))  # True (bo 5)
print(all([True, True, False]))  # False

slowa = ["kot", "pies", ""]
print(all(slowa))  # False (bo jest pusty string)

print(all(x % 2 == 0 for x in [2, 4, 6]))  # True (wszystkie parzyste)


# --- zip() ---


# zip() łączy kilka kolekcji w pary/trójki.
# Zwraca iterator → zamieniamy na listę/tuple/dict.
imiona = ["Ala", "Ola", "Jan"]
wiek = [25, 30, 40]
miasta = ["Poznań", "Warszawa", "Kraków"]
pary = list(zip(imiona, wiek))
print(pary)  # [('Ala', 25), ('Ola', 30), ('Jan', 40)]

trojki = list(zip(imiona, wiek, miasta))
print(trojki)  # [('Ala', 25, 'Poznań'), ('Ola', 30, 'Warszawa'), ('Jan', 40, 'Kraków')]

for name, age in zip(imiona, wiek):
    print(f"{name} ma {age} lat.")


# --- reduce() ---


# reduce() – składa całą kolekcję do jednej wartości.
# Funkcja bierze dwa argumenty: poprzedni wynik i nowy element.
from functools import reduce
liczby = [1, 2, 3, 4]
suma = reduce(lambda a, b: a + b, liczby)
print(suma)  # 10

iloczyn = reduce(lambda a, b: a * b, liczby)
print(iloczyn)  # 24

max_val = reduce(lambda a, b: a if a > b else b, liczby)
print(max_val)  # 4
