"""
Ćwiczenia – Funkcje + SP01 (sekcje 4–16)
"""

print("Ćwiczenia: Funkcje + SP01")
print("="*40)

# ------------------------------------------------------------
# 1. Parzysta czy nieparzysta
# Napisz funkcję is_even(n), która sprawdzi czy liczba jest parzysta.
# Wejście: liczba całkowita z input().
# Wyjście: True / False
# TODO: 

def is_even(x):
    return x % 2 == 0
        
x = int(input("podaj liczbę: "))
print(is_even(x))
print("-"*40)




# ------------------------------------------------------------
# 2. Największa liczba z listy
# Funkcja find_max(lista) ma zwrócić największy element listy.
# Wersja 1: użyj max()
# Wersja 2: bez max(), użyj pętli for.
# TODO: 

def find_max(lista):
    if not lista:
        return "Pusta lista"
    return max(lista)

lista = [1,2,3,4,5,6,64,22,31]
print(find_max(lista))
print("-"*40)



def find_max_for(lista):
    if not lista:
        return "Pusta lista"
    najwieksza = lista[0]
    for i in lista:
        if i > najwieksza:
            najwieksza = i
    return najwieksza


print(find_max_for(lista))
print("-"*40)




# ------------------------------------------------------------
# 3. Suma i średnia
# Funkcja suma_srednia(lista) -> "Suma: X, Średnia: Y"
# Zabezpiecz się przed pustą listą.
# Zaokrąglij średnią do 2 miejsc po przecinku.
# TODO: 

def suma_srednia(lista):
    if not lista :
        return "Suma: 0, Średnia 0"
    else:
        return f"Suma: {sum(lista)}, Średnia: {(sum(lista) / len(lista)):.2f}"
    
lista = [3,2,4,1,2,5,3]    
print(suma_srednia(lista))
print("-"*40)




# ------------------------------------------------------------
# 4. Filtrowanie listy
# Z listy [1..9] wybierz tylko nieparzyste.
# a) filter() + lambda
# b) list comprehension
# TODO: 

lista = [1,2,3,4,5,6,7,8,9]
nieparzyste = [n for n in lista if n % 2 == 1]
print(nieparzyste)
print("-"*40)


print(list(filter(lambda n: n % 2 == 1, lista))) 
print("-"*40)


# ------------------------------------------------------------
# 5. Sortowanie po ostatniej literze
# Lista = ["kot", "pies", "zebra", "lew", "słoń"]
# a) Użyj sorted()
# b) Zrób comprehension zwracające same ostatnie litery w tej kolejności
# TODO: 

lista = ["kot", "pies", "zebra", "lew", "słon"]
sorted_lista = sorted(lista, key = lambda x: x[-1])
print(sorted_lista)

sorted_comp = [x[-1] for x in sorted_lista ]
print(sorted_comp)
print("-"*40)


# ------------------------------------------------------------
# 6. Średnia z input()
# Pobierz od użytkownika 3 liczby oddzielone przecinkami, np. "10,20,30".
# Zamień na listę intów, policz średnią.
# TODO: 
"""
x = [int(x.strip()) for x in input("Podaj 3 liczby oddzielone przecinkami, naciśnij enter: ").split(",")]
srednia = sum(x) / len(x)
print(f"Średnia: {srednia:.2f}")
print("-"*40)
"""

# Wersja z walidacją danych i obsługą błędów.

raw = input("Podaj 3 liczby po przecinkach: ")
parts = [p.strip() for p in raw.split(",")]
if len(parts) != 3:
    print("Podaj dokładnie 3 liczby.")
else:
    try:
        nums = [int(p) for p in parts]
        print(f"Średnia: {sum(nums)/len(nums):.2f}")
    except ValueError:
        print("Błąd: wpisz tylko liczby całkowite.")


# Pobieramy dane od użytkownika w postaci tekstu (string).
# Użytkownik ma wpisać liczby rozdzielone przecinkami, np. "10, 20, 30".
# raw = input("Podaj 3 liczby po przecinkach: ")

# Rozdzielamy tekst po przecinkach -> powstaje lista stringów.
# "10, 20, 30" -> ["10", " 20", " 30"]
# Dodatkowo używamy .strip(), żeby usunąć spacje z przodu/tyłu każdego elementu.
# parts = [p.strip() for p in raw.split(",")]

# Walidacja: sprawdzamy, czy użytkownik podał dokładnie 3 liczby.
# Jeśli nie (np. podał tylko 2 albo 5), to kończymy i wyświetlamy komunikat.
# if len(parts) != 3:
#    print("Podaj dokładnie 3 liczby.")
# else:
#   try:
        # Próbujemy zamienić elementy listy na liczby całkowite (int).
        # ["10", "20", "30"] -> [10, 20, 30]
#        nums = [int(p) for p in parts]

        # Jeśli się udało, liczymy średnią.
        # sum(nums) = suma liczb, len(nums) = ilość elementów w liście.
#       print(f"Średnia: {sum(nums)/len(nums):.2f}")

#    except ValueError:
        # Jeśli podczas zamiany na int wystąpi błąd (np. ktoś wpisze "abc"),
        # to program nie wywali się, tylko pokaże komunikat błędu.
#        print("Błąd: wpisz tylko liczby całkowite.")


print("-"*40)



# ------------------------------------------------------------
# 7. Kwadraty liczb
# Funkcja kwadraty(lista) zwraca listę kwadratów elementów.
# a) map() + lambda
# b) list comprehension
# TODO: 

def kwadraty(lista):
    return list(map(lambda x: x**2, lista))

lista = [1,2,3,4,5,6]
print(kwadraty(lista))
print("-"*40)

kwadraty_comp = [x**2 for x in lista]
print(kwadraty_comp)
print("-"*40)



# ------------------------------------------------------------
# 8. Zip – łączenie danych
# imiona = ["Anna", "Paweł", "Kasia"]
# wiek   = [20, 25, 30]
# a) Połącz w krotki (imię, wiek) → zip()
# b) Zbuduj słownik {imię: wiek} comprehension
# TODO: 

imiona = ["Anna", "Paweł", "Kasia"]
wiek   = [20, 25, 30]
polaczone = tuple(zip(imiona, wiek))
print(polaczone)
print("-"*40)


x = {i:w for i,w in zip(imiona,wiek)}
print(x)
print("-"*40)



# ------------------------------------------------------------
# 9. Slice i slice assignment
# liczby = [0,1,2,3,4,5,6,7,8,9]
# a) Wypisz co drugi element 
# b) Zamień fragment [3:6] na [99,100]
# TODO: 
liczby = [0,1,2,3,4,5,6,7,8,9]

print(liczby[::2])
liczby[3:6] = [99,100]
print(liczby)
print("-"*40)



# ------------------------------------------------------------
# 10. Dict comprehension
# imiona = ["Ala", "Robert", "Ola"]
# a) Zbuduj słownik {imię: długość_imienia}
# b) Dodaj filtr → tylko imiona zaczynające się na "A"
# TODO: 

imiona = ["Ala", "Robert", "Ola"]
name_len = {x:len(x) for x in imiona}
print(name_len)
print("-"*40)


set_dic_filter = {x:len(x)for x in imiona if x[0].upper() == "A"}
print(set_dic_filter)


print("="*40)

