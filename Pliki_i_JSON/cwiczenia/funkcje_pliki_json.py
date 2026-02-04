# ============================================
# 1. Suma liczb dodatnich
# Napisz funkcję, która przyjmuje listę liczb.
# Zwróć sumę tylko tych liczb, które są dodatnie.
# Użyj list comprehension.
# TODO

def positive_sum(numbers):
    if not numbers:
        raise ValueError("Pusta lista")
    return sum(x for x in numbers if x >= 0)


numbers = [1,2,3,-5,-6,-2,4,5]
print(positive_sum(numbers))
# Cel: Zwrócić sumę liczb nieujemnych z listy.
# Jak działa:
# - if not numbers: sprawdza przypadek pustej listy.
# - sum(x for x in numbers if x >= 0): składanie generatorowe – sumujemy tylko te x, które są >= 0.


print("="*40)


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
# Cel: Dla liczby >= 0 zwraca "Parzysta"/"Nieparzysta"; dla ujemnej – raise ValueError.
# Jak działa:
# - if a is None: łapiesz brak wartości (None) – słusznie.
# - a < 0 → raise ValueError("liczba ujemna").
# - a % 2 == 0 → parzysta; w przeciwnym razie nieparzysta.
# Dobre praktyki:
# - Nazwa: lepsza byłaby np. is_even_label albo parity_label (czytelność).
# - Jeśli funkcja może otrzymać typ inny niż int, rozważ walidację typu lub rzutowanie.

print("="*40)


# ============================================

# ============================================
# 3. Zapis do pliku TXT
# Funkcja przyjmuje string i zapisuje go do pliku "output.txt".
# Jeśli string pusty → raise ValueError.
# TODO


def write_to_file(path, line):
    if not line:
        raise ValueError("Pusty tekst")
    with open(path, "w", encoding="utf-8") as f:
        f.write(line)
try:
    line = "Przykładowy tekst\n"
    write_to_file(r"../pliki_przykladowe/output.txt", line)
    print("Zapis do pliku udany.")
except ValueError as e:
    print(f"Bład: {e}")
# Cel: Zapisuje podany tekst do pliku (nadpisuje).
# Jak działa:
# - if not line: zabezpiecza przed pustym stringiem i rzuca ValueError.
# - with open(..., "w", encoding="utf-8"): otwiera plik w trybie zapisu (tworzy lub nadpisuje).
# - f.write(line): zapis treści.


print("="*40)



# ============================================

# ============================================
# 4. Odczyt z pliku TXT
# Funkcja wczytuje zawartość pliku "output.txt".
# Jeśli plik nie istnieje → obsłuż wyjątek.
# Jeśli plik pusty → raise ValueError.
# TODO

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

        if not content:
            raise ValueError("plik pusty")
        return content
    
try:
    print(read_file("../pliki_przykladowe/output.txt"))
except FileNotFoundError:
    print("Brak pliku")
except ValueError as e:
    print(f"Błąd: {e}")
# Cel: Odczytuje cały plik tekstowy i zwraca jego zawartość.
# Jak działa:
# - f.read(): wczytuje całość do stringa.
# - if not content: pusty plik → raise ValueError ("plik pusty").
# Wyjątki:
# - FileNotFoundError łapiesz na zewnątrz w bloku try/except – to poprawny podział odpowiedzialności:
#   funkcja „mówi prawdę” (czyta i zwraca), a UI/warstwa wyżej decyduje jak zareagować.

print("="*40)





# ============================================

# ============================================
# 5. JSON – zapis konfiguracji
# Funkcja zapisuje słownik {"user": ..., "lang": ...} do pliku config.json.
# Jeśli słownik nie ma klucza "user" → raise KeyError.
# TODO
import json

def write_dict(path, data):
    if "user" not in data:
        raise KeyError("Brak klucza 'user' ")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
data = {"user": "Robert", "lang": "PL", "age": 43}
try:
    write_dict(r"../pliki_przykladowe/config.json", data)
    print("Zapisano config.json")
except (KeyError, ValueError) as e:
    print(f"Błąd: {e}")
except FileNotFoundError as e:
    print(f"Brak pliku, wystąpił błąd: {e}")
# Cel: Zapisuje słownik jako ładny JSON (UTF-8, wcięcia).
# Jak działa:
# - if "user" not in data: wymagany klucz → brak → KeyError.
# - json.dump(data, f, ensure_ascii=False, indent=4): zapisuje słownik do pliku w formacie JSON,
#   z polskimi znakami (ensure_ascii=False) i czytelnymi wcięciami (indent=4).



print("="*40)

# ============================================

# ============================================
# 6. JSON – odczyt konfiguracji
# Funkcja otwiera plik config.json i wczytuje dane do słownika.
# Obsłuż: brak pliku, pusty plik, błędny JSON.
# TODO
import json

def read_json_file(path):
    with open(path, "r", encoding="utf-8") as f:
        raw_content = f.read()
        if not raw_content:
            raise ValueError("Plik pusty")
        try:
            parsed_data = json.loads(raw_content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Błędne dane w pliku, bład: {e}")
        return parsed_data
# ---
# WERSJA ALTERNATYWNA (krótsza, częściej w pracy):
#
# def read_json_file(path):
#     with open(path, "r", encoding="utf-8") as f:
#         try:
#             return json.load(f)   # tutaj nie robimy .read(), tylko od razu przekazujemy plik
#         except json.JSONDecodeError as e:
#             raise ValueError(f"Błędne dane w pliku, błąd: {e}")
#
# Uwaga: w tej wersji nie ma prostego sprawdzenia pustego pliku – 
#       do tego trzeba by np. sprawdzić rozmiar pliku przed otwarciem.
# ---
    
try:
    print("Plik wczytano poprawnnie: ")
    print(read_json_file(r"../pliki_przykladowe/config.json"))
except FileNotFoundError:
    print("Pliku nie zanleziono")
except ValueError as e:
    print(f"Błąd: {e}")
# Cel: Wczytuje plik JSON do obiektu Pythona (dict/list), obsługuje puste pliki i błędny JSON.
# Jak działa (WERSJA 1 – „edukacyjna”):
# - f.read() → raw_content (surowy tekst JSON).
# - if not raw_content: pusty plik → raise ValueError("Plik pusty").
# - try: json.loads(raw_content) → parsowanie stringa na strukturę Pythona.
#   except json.JSONDecodeError: błędna składnia JSON → raise ValueError z opisem błędu.
# WERSJA 2 (zakomentowana) – „produkcyjna skrócona”:
# - json.load(f) – przekazujesz od razu plik, bez ręcznego f.read().
# - Plus: krócej i czytelniej; Minus: trudniej sprawdzić „pustkę” bezpośrednio.
# Dobre praktyki:
# - Do konfiguracji w projektach najczęściej używa się json.load(f).
# - Gdy masz JSON jako string (np. z API), wtedy json.loads(s).




print("="*40)

# ============================================

# ============================================
# 7. Najdłuższe słowo
# Funkcja przyjmuje listę stringów i zwraca najdłuższy element.
# Jeśli lista pusta → raise ValueError.
# Wykorzystaj wbudowaną funkcję max() z parametrem key=len.
# TODO

def longest_words(lista):
    if not lista:
        raise ValueError("Błąd, pusta lista")
    
    max_len = max(len(word) for word in lista)
    return [word for word in lista if len(word) == max_len]
    
lista = ["Dupa", "maryna", "cimcirimcim", "kotopies", "tojestwyraz"]    
try:
    print(f" Najdłuższe słowo z listy: {longest_words(lista)}")
except ValueError as e:
    print(f"Błąd: {e}")
except Exception as e:
    print(f"Wystąpił nieoczekiwany błąd: {e}")
# Cel: Zwraca wszystkie słowa o maksymalnej długości (lista wynikowa może mieć 1 lub więcej elementów).
# Jak działa:
# - if not lista: raise ValueError (pusta lista).
# - max_len = max(len(word) for word in lista): najpierw znajdujesz największą długość (liczbę).
# - return [word for word in lista if len(word) == max_len]: filtrujesz te słowa, które mają tę długość.
# Alternatywa:
# - Jeśli chcesz zwrócić JEDNO najdłuższe słowo: return max(lista, key=len).
# - Jeśli chcesz wszystkie – zostaw jak jest (Twoja wersja obsługuje remisy długości).



print("="*40)

# ============================================

# ============================================
# 8. Funkcja anonimowa (lambda)
# Utwórz lambdę, która przyjmuje liczbę i zwraca jej kwadrat.
# Przetestuj ją na kilku liczbach za pomocą map().
# TODO
import random


square_range = list(map(lambda x: x**2, range(1, 10)))
print(square_range)

nums = [random.randint(1,20) for _ in range(5)]
squares = list(map(lambda x: x**2, nums))

print(f"Liczby: {nums}")
print(f"Kwadraty: {squares}")
# Cel: Pokazać lambdę i map().
# Jak działa:
# - list(map(lambda x: x**2, range(1, 10))): tworzy listę kwadratów 1..9.
# - nums = [random.randint(1,20) for _ in range(5)]: losowe 5 liczb 1..20.
# - squares = list(map(lambda x: x**2, nums)): kwadraty wylosowanych liczb.
# Dobre praktyki:
# - map()/filter() są OK, ale w Pythonie często czytelniejsze są list comprehensions: [x**2 for x in nums].



print("="*40)

# ============================================

# ============================================
# 9. Filtrowanie liczb
# Funkcja przyjmuje listę liczb i zwraca nową listę z tylko parzystymi.
# Użyj funkcji filter() + lambdy.
# TODO


def filtered_nums(lista):
    return list(filter(lambda x: x % 2 ==0, lista))
    

lista = [1,2,3,6,5,4,5,8,9,7,4,2,5,6,3,2,1,12]
print(filtered_nums(lista))
# Cel: Zwraca listę elementów parzystych.
# Jak działa:
# - filter(lambda x: x % 2 == 0, lista) → iterator tylko z parzystymi; list(...) → lista wynikowa.
# Wariant „pythoniczny”:
# - [x for x in lista if x % 2 == 0] – zwykle bardziej czytelne.



print("="*40)

# ============================================

# ============================================
# 10. Generator haseł
# Funkcja tworzy losowe hasło o zadanej długości.
# Użyj modułu random.choice i string.ascii_letters + digits.
# Jeśli długość < 4 → raise ValueError.
# Zapisz wygenerowane hasło do pliku "password.txt".
# TODO
import random
import string

def password_generator(length):
    if length < 4:
        raise ValueError("Zbyt krótkie hasło")   
    
    znaki = string.ascii_letters + string.digits
    haslo = ""

    for i in range(length):
        haslo += random.choice(znaki)
    with open(r"../pliki_przykladowe/password.txt", "w", encoding="utf-8") as f:
        f.write(haslo)
    return haslo
    
length = 8
print(password_generator(length))
# Cel: Zbudować losowe hasło o zadanej długości i zapisać do pliku.
# Jak działa:
# - if length < 4: raise ValueError – minimalna sensowna długość (tu: 4).
# - znaki = string.ascii_letters + string.digits: dozwolony alfabet (A-Z, a-z, 0-9).
# - haslo = "" i pętla for i in range(length): w każdej iteracji doklejasz losowy znak z „znaki”.
# - random.choice(znaki): wybiera pojedynczy znak z alfabetu.
# - with open(..., "w", encoding="utf-8"): zapisuje gotowe hasło do pliku "../pliki_przykladowe/password.txt".
# - return haslo: zwracasz hasło (możesz je też wydrukować).
# UWAGA – bezpieczeństwo:
# - Moduł random NIE jest kryptograficznie bezpieczny. Do prawdziwych haseł używaj modułu „secrets”:
#     import secrets
#     secrets.choice(znaki)  # zamiast random.choice
# - Rozważ poszerzenie alfabetu o znaki specjalne (string.punctuation), jeśli projekt tego wymaga.
# - Zapisywanie hasła w pliku wprost to ryzyko (plaintext). W praktyce:
#     – trzymaj w menedżerze haseł,
#     – jeśli musisz zapisać, zadbaj o prawa dostępu/bezpieczne miejsce,
#     – lub zapisuj hash, nie jawne hasło (zależnie od celu ćwiczenia).
# Dobre praktyki:
# - Parametryzacja: rozważ przyjmowanie też „alphabet” (zestawu znaków) i „output_path” jako argumentów,
#   żeby funkcja była bardziej wielokrotnego użytku.
# - Testowalność: funkcja ma efekt uboczny (zapis do pliku). W testach łatwiej, gdy rozdzielisz:
#     a) generate_password(length, alphabet) → tylko zwraca string,
#     b) save_password(path, password) → zapis do pliku.
#   Dzięki temu logikę losowania testujesz osobno, a I/O osobno.









print("="*40)

# ============================================
