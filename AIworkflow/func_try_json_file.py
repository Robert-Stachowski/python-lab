# ============================================
# 1. Suma liczb dodatnich
# Napisz funkcję, która przyjmuje listę liczb.
# Zwróć sumę tylko tych liczb, które są dodatnie.
# Użyj list comprehension.
# TODO

def positive_sum(numbers):
    if not numbers:
        return ValueError("Pusta lista")
    return sum(x for x in numbers if x >= 0)


numbers = [1,2,3,-5,-6,-2,4,5]
print(positive_sum(numbers))



# ============================================

# ============================================
# 2. Parzysta czy nieparzysta
# Funkcja przyjmuje liczbę. Jeśli jest ujemna → raise ValueError.
# Jeśli >= 0, zwróć napis "parzysta" albo "nieparzysta".
# TODO

def wtf_numer(a):
    if a is None:
        raise ValueError("Brak liczby")
    elif a < 0:
        raise ValueError("liczba ujemna")
    elif a % 2 == 0:
        return ("Parzysta")
    else:
        return ("Nieparzysta")

try:
    print(wtf_numer(0))
except ValueError as e:
    print(f"Błąd: {e}")



# ============================================

# ============================================
# 3. Zapis do pliku TXT
# Funkcja przyjmuje string i zapisuje go do pliku "output.txt".
# Jeśli string pusty → raise ValueError.
# TODO






# ============================================

# ============================================
# 4. Odczyt z pliku TXT
# Funkcja wczytuje zawartość pliku "output.txt".
# Jeśli plik nie istnieje → obsłuż wyjątek.
# Jeśli plik pusty → raise ValueError.
# TODO
# ============================================

# ============================================
# 5. JSON – zapis konfiguracji
# Funkcja zapisuje słownik {"user": ..., "lang": ...} do pliku config.json.
# Jeśli słownik nie ma klucza "user" → raise KeyError.
# TODO
# ============================================

# ============================================
# 6. JSON – odczyt konfiguracji
# Funkcja otwiera plik config.json i wczytuje dane do słownika.
# Obsłuż: brak pliku, pusty plik, błędny JSON.
# TODO
# ============================================

# ============================================
# 7. Najdłuższe słowo
# Funkcja przyjmuje listę stringów i zwraca najdłuższy element.
# Jeśli lista pusta → raise ValueError.
# Wykorzystaj wbudowaną funkcję max() z parametrem key=len.
# TODO
# ============================================

# ============================================
# 8. Funkcja anonimowa (lambda)
# Utwórz lambdę, która przyjmuje liczbę i zwraca jej kwadrat.
# Przetestuj ją na kilku liczbach za pomocą map().
# TODO
# ============================================

# ============================================
# 9. Filtrowanie liczb
# Funkcja przyjmuje listę liczb i zwraca nową listę z tylko parzystymi.
# Użyj funkcji filter() + lambdy.
# TODO
# ============================================

# ============================================
# 10. Generator haseł
# Funkcja tworzy losowe hasło o zadanej długości.
# Użyj modułu random.choice i string.ascii_letters + digits.
# Jeśli długość < 4 → raise ValueError.
# Zapisz wygenerowane hasło do pliku "password.txt".
# TODO
# ============================================
