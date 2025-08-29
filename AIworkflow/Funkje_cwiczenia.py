from functools import reduce

liczby = [1, 2, 3, 4]
iloczyn = reduce(lambda a, b: a * b, liczby)
print(iloczyn)
print("-----------------------------------")

# 1
x = int(input("Podaj liczbę: "))
cube = lambda x: x**3
print(cube(x))
print("-----------------------------------")


# 2
lista = [10,20,30]
napis = list(map(str, lista))                   # tu zamieniamy listę na string!
print(napis)

a = [str(x) for x in lista]                     # list comprehension
print(a)
print("-----------------------------------")

# 3
lista_1 = [1,2,3,4,5,6,7,8,9]
nieparzyste = list(filter(lambda x: x % 2 == 1, lista_1))       # Szukanie liczb NIEPARZYSTYCH
print(nieparzyste)

comp = [x for x in lista_1 if x % 2 ==1]                        # list comprehension
print(comp)
print("-----------------------------------")

# 4
lista_2 = ["kot", "pies", "zebra", "lew", "slon"]
ostatnia_litera = sorted(lista_2, key = lambda x: x[-1])  # Sortowanie po ostatniej literze elementu
print(ostatnia_litera)

lista_comp = [x[-1] for x in lista_2]                         # Tu list comprehension wyciąga tylko ostatnie litery z elementów listy
print(lista_comp)

lista_sorted = [x[-1] for x in sorted(lista_2, key = lambda x: x[-1])]      # sorted() + comprehension
print(lista_sorted)
# Schemat działania: sorted + comprehension
#
# Mamy listę:
# ["kot", "pies", "zebra", "lew", "slon"]
#
# 1. sorted(lista, key=lambda char: char[-1])
#    - Funkcja key decyduje, według czego sortujemy.
#    - char[-1] oznacza: weź ostatnią literę słowa.
#    - Wynik sortowania po ostatniej literze:
#      ["zebra", "slon", "pies", "kot", "lew"]
#
# 2. [x[-1] for x in ...]
#    - Comprehension buduje nową listę.
#    - x[-1] oznacza: weź ostatnią literę z każdego słowa.
#    - Wynik końcowy:
#      ['a', 'n', 's', 't', 'w']
#
# Podsumowanie:
# - Pierwsze [-1] w lambda -> określa kolejność sortowania.
# - Drugie [-1] w comprehension -> wybiera, co finalnie trafia do listy.




