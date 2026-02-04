# ===========================================
# Ćwiczenia utrwalające
# ===========================================

# 1. Użyj math do policzenia 5! (silnia).
# 2. Użyj random do wylosowania hasła z listy ["Python", "Django", "Backend"].
# 3. Sprawdź status strony https://google.com i wypisz czy jest OK.
# 4. Stwórz plik requirements.txt i zapisz w nim nazwę modułu requests.
# 5. Narzędzia odkrywania funkcji i klas w module.

import random as rn
import math
import requests as rq


# 1

try:
    x = int(input("podaj liczbę: "))

    if x < 0:
        raise ValueError("Silnia jest zdefiniowana tylko dla liczb >= 0")
    if x > 20:
        raise ValueError("Za duża liczba - ogranicz do max 20!")

    silnia = 1
    for i in range(1, x + 1):    
            silnia *= i
        
    print(f"{x}! = {silnia}")


except ValueError as e:
     print(f"Błąd! {e}")
print("-"*50)

# Math

print(f"Silnia = {math.factorial(x)}")
print("-"*50)




# 2

print(rn.choice(["Python", "Django", "Backend"]))
print("-"*50)



# 3


response = rq.get("https://google.com")
print(response.status_code)
print("-"*50)



# 4

# Done :)



# 5

print(dir(math)) # lista nazw dostępnych w module, np. 'sqrt', 'pi', 'ceil', ...
help(math.sqrt) # opis funkcji: argumenty, przeznaczenie, uwagi
help(math) # ogólny opis całego modułu
wynik = math.sqrt(16)
print(type(wynik)) # np. <class 'float'>





