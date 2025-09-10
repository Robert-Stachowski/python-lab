# =====================================================
# Moduły wbudowane i zewnętrzne w Pythonie, podstawowe.
# =====================================================



# --- Moduł math ---

import math

print("Math examples:")
print(math.sqrt(16))     # 4.0 – pierwiastek kwadratowy (square root)
print(math.pow(2, 3))    # 8.0 – potęgowanie (power)
print(math.pi)           # 3.14159... – stała π
print(math.factorial(5)) # 120 – silnia z liczby 5
print(math.floor(3.9))   # 3 – zaokrąglenie w dół
print(math.ceil(3.1))    # 4 – zaokrąglenie w górę



# --- Moduł random ---

import random

print("\nRandom examples:")
print(random.randint(1, 10))   # losowa liczba całkowita od 1 do 10
print(random.choice(["kot", "pies", "koń"]))  # losowy wybór elementu z listy
print(random.random())         # losowa liczba z zakresu 0.0 – 1.0

lista = [1, 2, 3, 4, 5]
random.shuffle(lista)          # tasowanie listy
print("Tasowana lista:", lista)



# --- Moduł zewnętrzny requests ---
# Aby zainstalować: pip install requests

import requests

print("\nRequests examples:")
response = requests.get("https://example.com")

if response.ok:  # sprawdzamy, czy zapytanie się udało (status 200–299)
    print("Status:", response.status_code)
    print("Fragment strony:", response.text[:100])  # pierwsze 100 znaków
else:
    print("Błąd przy pobieraniu strony:", response.status_code)
