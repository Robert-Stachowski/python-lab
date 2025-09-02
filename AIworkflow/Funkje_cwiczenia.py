"""

## 🔹 Ćwiczenia

1. **Kwadrat liczby (lambda)**
   Napisz funkcję lambda, która dla podanej liczby zwróci jej **sześcian**. Sprawdź dla `2` i `5`.

2. **map() – konwersja na stringi**
   Masz listę liczb `[10, 20, 30]`. Użyj `map()` i `str`, żeby zamienić wszystkie na napisy: `["10", "20", "30"]`.

3. **filter() – nieparzyste**
   Z listy `[1, 2, 3, 4, 5, 6, 7]` wyciągnij tylko liczby nieparzyste.

4. **sorted() – sortowanie po ostatniej literze**
   Masz listę `["kot", "pies", "zebra", "lew"]`. Posortuj ją wg **ostatniej litery**.

5. **reduce() – iloczyn elementów**
   Za pomocą `reduce()` pomnóż wszystkie elementy listy `[2, 3, 4, 5]`.

6. **any() – sprawdzanie**
   Sprawdź za pomocą `any()`, czy w liście `[0, 0, 0, 1]` znajduje się przynajmniej jedna liczba różna od zera.

7. **all() – walidacja**
   Masz listę `["Ala", "Ola", "Jan"]`. Użyj `all()`, aby sprawdzić, czy wszystkie elementy są niepuste.

8. **zip() – łączenie danych**
   Połącz listy: imiona `["Anna", "Paweł", "Kasia"]` i wiek `[20, 25, 30]` w listę krotek.

9. **sum() – tylko parzyste**
   Z listy `[1, 2, 3, 4, 5, 6]` policz sumę **tylko parzystych** elementów.

10. **abs() + round() – odległość**
    Masz liczby zmiennoprzecinkowe: `[-3.14159, 2.718, -1.414]`.

    * Najpierw policz ich wartość bezwzględną (abs).
    * Następnie zaokrąglij każdą do 2 miejsc po przecinku.


"""


from functools import reduce


print("-----------------------------------")
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
print(f"{ostatnia_litera}                            #Sorted")

lista_comp = [x[-1] for x in lista_2]                         # Tu list comprehension wyciąga tylko ostatnie litery z elementów listy, bez sortowania
print(f"{lista_comp}                                          #Comprehension")

lista_sorted = [x[-1] for x in sorted(lista_2, key = lambda x: x[-1])]      # sorted() + comprehension
print(f"{lista_sorted}                                          #Sorted+Comprehension")
print("-----------------------------------")

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



# 5

lista = [1,2,3,4,5,6]
iloczyn = reduce(lambda a, b : a*b, lista)
print(iloczyn)
print("-----------------------------------")
# Schemat działania reduce dla iloczynu:
#
# lista = [1, 2, 3, 4, 5, 6]
#
# reduce(lambda a, b: a * b, lista)
#
# Działa krokami:
# 1. (1 * 2) = 2
# 2. (2 * 3) = 6
# 3. (6 * 4) = 24
# 4. (24 * 5) = 120
# 5. (120 * 6) = 720
#
# Wynik końcowy = 720
#
# Ważne:
# - List comprehension nie nadaje się do akumulacji (tylko do tworzenia list).
# - Alternatywy: pętla for z akumulatorem albo math.prod(lista).


# 6

lista = [0, 0, 0, 1]
print(any(lista))
print("-----------------------------------")

# Schemat działania any():
#
# lista = [0, 0, 0, 1]
#
# any(lista) sprawdza:
# - Czy JAKIKOLWIEK element listy jest "prawdziwy" (True)?
# - 0 jest traktowane jako False, a 1 jako True.
#
# Sprawdzenie krok po kroku:
# [0, 0, 0, 1] → [False, False, False, True]
#
# Ponieważ występuje True → wynik końcowy = True



# 7

lista = ["Ala", "Ola", "Jan"]
print(all(lista))
print("-----------------------------------")
# Schemat działania all():
#
# lista = ["Ala", "Ola", "Jan"]
#
# all(lista) sprawdza:
# - Czy WSZYSTKIE elementy listy są "prawdziwe" (True)?
# - W Pythonie: pusty string "" = False, niepusty string = True.
#
# Sprawdzenie krok po kroku:
# ["Ala", "Ola", "Jan"] → [True, True, True]
#
# Ponieważ wszystkie elementy są True → wynik końcowy = True



# 8

imiona = ["Anna", "Paweł", "Kasia"]
wiek = [20, 25, 30]
razem = tuple(zip(imiona, wiek))
print(razem)
print("-----------------------------------")
# Schemat działania zip():
#
# imiona = ["Anna", "Paweł", "Kasia"]
# wiek   = [20, 25, 30]
#
# zip(imiona, wiek) łączy elementy "po indeksach":
# - (imiona[0], wiek[0]) -> ("Anna", 20)
# - (imiona[1], wiek[1]) -> ("Paweł", 25)
# - (imiona[2], wiek[2]) -> ("Kasia", 30)
#
# Wynik: [("Anna", 20), ("Paweł", 25), ("Kasia", 30)]
# (tu zamienione na tuple -> (('Anna', 20), ('Paweł', 25), ('Kasia', 30)))
#
# Ważne:
# - zip działa tylko do najkrótszej listy (jeśli długości różne).


# 9

lista = [1, 2, 3, 4, 5, 6]
suma_parzystych = sum(x for x in lista if x % 2 == 0)
print(suma_parzystych)
print("-----------------------------------")
# Schemat działania sum() z warunkiem:
#
# lista = [1, 2, 3, 4, 5, 6]
#
# sum(x for x in lista if x % 2 == 0)
#
# Krok po kroku:
# - Sprawdzamy każdy element listy:
#   1 % 2 == 0 -> False (pomijamy)
#   2 % 2 == 0 -> True  (dodajemy 2)
#   3 % 2 == 0 -> False
#   4 % 2 == 0 -> True  (dodajemy 4)
#   5 % 2 == 0 -> False
#   6 % 2 == 0 -> True  (dodajemy 6)
#
# Suma = 2 + 4 + 6 = 12
#
# Ważne:
# - "x for x in lista if ..." to tzw. generator expression.


# 10

lista = [-3.14159, 2.718, -1.414]
lista_abs = [abs(x) for x in lista]
lista_round = [round(x, 2) for x in lista_abs]
print(lista_abs)
print(lista_round)
print("-----------------------------------")
# Schemat działania abs() + round():
#
# lista = [-3.14159, 2.718, -1.414]
#
# 1. [abs(x) for x in lista]
#    - abs() zwraca wartość bezwzględną (usuwa znak minus).
#    - Wynik: [3.14159, 2.718, 1.414]
#
# 2. [round(x, 2) for x in lista_abs]
#    - round(x, 2) zaokrągla liczbę do 2 miejsc po przecinku.
#    - Wynik: [3.14, 2.72, 1.41]
#
# Efekt końcowy:
# wartości bezwzględne liczb zaokrąglone do 2 miejsc po przecinku


print(type(3.14))       # <class 'float'>
print("-----------------------------------")

x = "hello"
print(x * 3)            # hellohellohello
print("-----------------------------------")

for i in range(3):
    print(i)            # 0 1 2

print("-----------------------------------")


for i in range(3):
    if i == 1:
        continue
    print(i)            # 0 2

print("-----------------------------------")

lista = ["ala","pies","f","fdfdsaass","gfds"]
new_lista = sorted(lista, key=lambda x: len(x))
print(new_lista)
print("-----------------------------------")


numbers = [1,2,3,4,5,6,7,8,9,10]
q = []
def average(numbers): 
   try:  
      for _ in numbers:        
         q = int(sum(numbers)) / int(len(numbers))
         return q
   except:
       ValueError
       
print(average(numbers))   
print("-----------------------------------")



list_1 = [1,2,3,4]
iloczyn = reduce(lambda a,b :a*b , list_1)
print(iloczyn)
print("-----------------------------------")



names = ["Ala", "Robert", "Ola"]
result = {name: len(name) for name in names}
print(result)
print("-----------------------------------")


a = set("python")
print(a)
print("-----------------------------------")


x = [int(x.strip()) for x in input("podaj 3 liczby").split(",")]
srednia = sum(x) / len(x)
print(srednia)
print("-----------------------------------")


x = 7
print(x > 5 and x < 10)
print("-----------------------------------")


print(float("3.14"))
print("-----------------------------------")



y = lambda a,b: a +" "+ b
print(y("Hello", "World")) 
print("-----------------------------------")
print("-----------------------------------")
print("Ćwiczenia: ")

"""

## 📝 Zadania – Funkcje + funkcje wbudowane

1. **Parzystość liczby**
   Napisz funkcję `is_even(n)`, która zwraca `True` jeśli liczba jest parzysta, a `False` w przeciwnym wypadku.
   Wykorzystaj operator modulo `%`.

---

2. **Największa liczba z listy**
   Napisz funkcję, która przyjmuje listę liczb i zwraca największą z nich.
   Użyj wbudowanej funkcji `max()`.

---

3. **Suma i średnia**
   Napisz funkcję, która przyjmuje listę liczb i zwraca **sumę** oraz **średnią** elementów.
   Skorzystaj z `sum()` i `len()`.

---

4. **Łączenie stringów**
   Napisz funkcję, która przyjmuje dwa napisy i zwraca je połączone w jeden z odstępem.
   Użyj `f-string` albo `join()`.

---

5. **Długość słowa**
   Napisz funkcję, która przyjmuje napis i zwraca jego długość.
   Skorzystaj z `len()`.

---

6. **Podniesienie do kwadratu**
   Napisz funkcję, która przyjmuje listę liczb i zwraca nową listę z każdą liczbą podniesioną do kwadratu.
   Spróbuj użyć `map()` i `lambda`.

---

7. **Minimalna wartość**
   Napisz funkcję, która przyjmuje listę liczb i zwraca najmniejszą wartość.
   Skorzystaj z `min()`.

---

8. **Sprawdzenie, czy słowo zaczyna się na literę „A”**
   Funkcja przyjmuje napis i zwraca `True`, jeśli zaczyna się od „A” lub „a”.
   Skorzystaj z metody `.startswith()` albo `.lower()`.

---

9. **Zliczanie elementów**
   Napisz funkcję, która przyjmuje listę i zwraca, ile elementów w niej jest.
   Skorzystaj z `len()`.

---

10. **Unikalne elementy**
    Napisz funkcję, która przyjmuje listę i zwraca zbiór unikalnych elementów.
    Skorzystaj z `set()`.
"""

def is_even(n):    
     return n % 2 == 0
       

n = int(input("podaj liczbę: "))
print(is_even(n))
print("-----------------------------------")
# lambda: is_even = lambda n: n % 2 == 0



def znajdz_max(lista):
   return max(lista)

liczby = [1,22,30,5,54,1,254,87]
print(znajdz_max(liczby))
print("-----------------------------------")
# lambda: znajdz_max = lambda lst: max(lst)



liczby = [1,22,30,5,54,1,254,87]
print(max(liczby))   # 254
print("-----------------------------------")


def suma_srednia(lista):
   if not lista:
       return "Suma: 0, Średnia: 0"
   return f"Suma: {sum(lista)}, Średnia: {sum(lista)}/{len(lista)}"
# if not lista → w Pythonie pusta lista ma wartość logiczną False, a lista z elementami to True.
# Więc not lista jest True, gdy lista jest pusta.
# Wtedy funkcja od razu kończy się return i zwraca tekst "Suma: 0, Średnia: 0".
# (unikasz dzielenia przez zero przy liczeniu średniej).

liczby = [1,2,3,5,6,785,21]
print(suma_srednia(liczby))
print("-----------------------------------")



def napisy(a,b):
   return f"{a} {b}"

print(napisy("Dupa", "Maryna"))
print("-----------------------------------")
# lambda: join_space = lambda a, b: f"{a} {b}"



def dlugosc(napis):
   return len(napis)

print(dlugosc("abrakadabra"))
print("-----------------------------------")
# lambda: length = lambda s: len(s)



def kwadrat(lista):   
      return list(map(lambda x: x**2 , lista))

liczby = [1,2,3,4,5,6,7,8,9]
print(kwadrat(liczby))
print("-----------------------------------")
# lambda: kwadrat = lambda lst: [x**2 for x in lst]



def najmniejsza(lista):   
      return min(lista)

liczby = [1,2,3,4,5,6,7,8,9]   
print(najmniejsza(liczby))
print("-----------------------------------")
# lambda: najmniejsza = lambda lst: min(lst)



def a_team(lista):
   return lista[:1].lower()== "a"
            
slowo = "Bleee"
print(a_team(slowo))
print("-----------------------------------")
# lambda: a_team = lambda s: (s[:1].lower() == "a")



def dlugosc(a):
   return len(a)

lista = [1,2,3,2,5,3,6,4,4,5,6,98]
print(dlugosc(lista))
print("-----------------------------------")
# lambda: dlugosc_listy = lambda lst: len(lst)



def uniqe(lista):
   return set(lista)

liiczby = [1,2,3,3,2,5,6,4,12,8,87,8,9]
print(uniqe(liiczby))
# lambda: unique = lambda lst: set(lst)






