"""

1. Poproś użytkownika o dwie liczby i wypisz wynik dzielenia. Obsłuż ValueError i ZeroDivisionError z czytelnymi komunikatami.

"""

# 1

def divide(a, b):
    # Funkcja przyjmuje dwie liczby (a, b) i zwraca wynik dzielenia a/b.
    # Jeśli b == 0, Python automatycznie rzuci wyjątek ZeroDivisionError.
    return a / b


while True:
    try:
        # Blok TRY = "spróbuj wykonać"
        # 1. Pobierz od użytkownika pierwszą liczbę (a) i zamień na int.
        #    Jeśli wpisze np. "abc", poleci ValueError.
        a = int(input("Podaj pierwszą liczbę: "))
        b = int(input("Podaj drugą liczbę: "))

        # 2. Spróbuj od razu podzielić a/b.
        #    Jeśli b == 0 → ZeroDivisionError.
        wynik = divide(a, b)

    except ValueError:
        # Blok EXCEPT = "obsłuż błąd"
        # Łapie sytuację, gdy użytkownik podał coś, czego nie da się zamienić na int.
        print("❌ Musisz podać liczbę całkowitą.")
        # continue = wróć do początku pętli i pytaj jeszcze raz
        continue

    except ZeroDivisionError:
        # Obsługa sytuacji, gdy ktoś wpisał 0 jako mianownik.
        print("❌ Nie dzielimy przez zero!")
        continue

    else:
        # ELSE = wykona się TYLKO wtedy, gdy w całym TRY nie poleciał żaden wyjątek.
        # Skoro jesteśmy tutaj, to znaczy:
        # - użytkownik podał poprawne liczby
        # - dzielenie się udało
        print(f"✅ Wynik: {wynik:.2f}")  # :.2f = zaokrąglenie do 2 miejsc po przecinku
        # break = zakończ pętlę while, bo mamy już poprawny wynik
        break

    finally:
        # FINALLY = wykonuje się ZAWSZE (czy był błąd, czy nie).
        # W tym przykładzie tylko informacyjny print,
        # ale w prawdziwych programach służy do "sprzątania" (np. zamknięcie pliku, rozłączenie bazy).
        print("ℹ️ Próba wykonania dzielenia zakończona, transmisja zakończona xD")





print("="*40)
print("1. Parzysta czy nieparzysta z walidacją")
# Opis: Pobierz od użytkownika liczbę całkowitą. Jeśli wpis błędny – pokaż komunikat i nie wywal programu.
# TODO: input -> int z try/except, w else wypisz "parzysta" lub "nieparzysta".

def parzysta_nieparzysta(a):
    return a % 2 == 0

while True:
    try:
        a = int(input("Podaj liczbę całkowitą: "))
        
    except ValueError:
        print("Błąd, podaj liczbę całkowitą: ")
        continue
    else: 
        if parzysta_nieparzysta(a):
            print(f"Liczba {a} jest parzysta")
            
        else:
            print(f"Liczba {a} jest nieparzysta")
        
        break
# [OPIS]
# Funkcja parzysta_nieparzysta(a) zwraca True dla liczb parzystych.
# Wejście od użytkownika walidujemy w pętli while:
# - w try robimy int(input(...)),
# - w except ValueError informujemy o złym formacie i ponawiamy,
# - w else (czyli przy sukcesie) wypisujemy informację i kończymy pętlę.



print("="*40)
print("2. Dzielenie z kontrolą dzielnika")
# Opis: Program pobiera dwie liczby całkowite od użytkownika i dzieli je przez siebie.
# Funkcja dziel(a, b) dodatkowo sprawdza, czy mianownik (b) nie jest równy zero.
# Jeśli b == 0, zostaje rzucony wyjątek ValueError z czytelnym komunikatem.
# W pętli while True mamy walidację danych wejściowych i obsługę wyjątków,
# tak aby program nigdy się nie wywalił, tylko poprosił użytkownika o poprawne dane.

def dziel(a, b):
    # Funkcja dzieli dwie liczby a / b.
    # Jeśli b == 0 → zamiast dzielenia rzucamy wyjątek ValueError.
    if b == 0:
        raise ValueError("Błąd, nie dzielimy przez 0 ")
    return a / b


while True:
    try:
        # 1. Pobierz liczby od użytkownika i zamień na int.
        a = int(input("Podaj pierwszą liczbę: "))
        b = int(input("Podaj drugą liczbę: "))
        
        # 2. Spróbuj wykonać dzielenie.
        wynik = dziel(a, b)
    except ValueError as e:
        # Obsługa dwóch sytuacji:
        # - użytkownik podał złe dane (np. "abc" zamiast liczby) → ValueError z int()
        # - użytkownik podał 0 jako mianownik → ValueError z dziel()
        print(e)
        # continue → wracamy na początek pętli i pytamy ponownie
        continue        
    else:   
        # ELSE wykona się tylko, jeśli w try nie było żadnych wyjątków.
        # Drukujemy wynik z zaokrągleniem do 2 miejsc po przecinku
        print(f"Dzielenie: {a} / {b} = {wynik:.2f}")
        # break → kończymy pętlę, bo udało się poprawnie policzyć
        break










print("="*40)
print("3. Wczytaj JSON z pliku")
# Opis: Spróbuj wczytać plik config.json. Gdy brak pliku – użyj domyślnych ustawień (słownik).
# TODO: try/except FileNotFoundError; w else wydrukuj "OK"; w finally posprzątaj, jeśli trzeba.

import json

try:
    with open("config.json", "r", encoding="utf-8") as file:
        data = json.load(file)
except (FileNotFoundError, PermissionError):
    print("Błąd! Używam domyślnych ustawień")
    data = {"theme": "light", "lang": "pl"}
except json.JSONDecodeError:
    print("Błędny JSON w config.json – używam domyślnych ustawień")
    data = {"theme": "light", "lang": "pl"}
else:
    print("Wczytano konfigurację.")
finally:
    print("Koniec próby wczytania konfiguracji")
# [OPIS]
# Próba wczytania konfiguracji z pliku:
# - open(..., "r") może rzucić FileNotFoundError lub PermissionError.
# - Jeśli błąd, ustawiamy domyślne ustawienia (dict).
# - else: informacja, że wczytano OK.
# - finally: komunikat porządkujący.
# Uwaga: jeśli używamy file.read(), 'data' będzie stringiem; jeśli json.load(), będzie dict.
# W realnym kodzie warto trzymać spójny typ (np. zawsze dict).

# ==============================
# JSON w Pythonie – ściąga:
# - json.load(file)  -> używamy, gdy wczytujemy dane BEZPOŚREDNIO z pliku .json
# - json.loads(str) -> używamy, gdy mamy JSON jako STRING (np. z internetu, API, bazy)
#
# Przykład:
# with open("plik.json", "r", encoding="utf-8") as f:
#     data = json.load(f)       # wynik: dict lub list
#
# s = '{"name": "Robert", "age": 34}'
# data = json.loads(s)          # wynik: dict {"name": "Robert", "age": 34}
#
# W praktyce -> dla plików ZAWSZE json.load()
# ==============================










print("="*40)
print("4. Parsowanie listy liczb")
# Opis: Użytkownik wpisuje liczby rozdzielone przecinkami. Zbuduj listę intów.
# TODO: try/except dla ValueError; poprawny przypadek -> policz sumę i średnią.


def suma(a,b):
    return a + b

def srednia(lista):
    return sum(lista) / len(lista)

while True:         
    raw = input("Podaj dwie liczby oddzielone przecinkami: ").replace(" ",",")           
    parts = [x.strip() for x in raw.split(",") if x.strip()]
    if len(parts) != 2:    
        print("Podaj dokładnie dwie liczby oddzielone przecinkiem lub spacją.")
        continue
    else:
        try:            
            nums = [int(p) for p in parts]        
        except ValueError:
            print("Podaj liczby całkowite")
            continue
        else:
            print(f"Suma wprowadzonych liczb: {suma(nums[0], nums[1])}")
            print(f"Średnia wprowadzonych liczb: {srednia(nums):.2f}")
            break
        

# -----------------------------------------------
# Program: suma i średnia z dwóch liczb z inputu
# Wejście: użytkownik wpisuje dwie liczby rozdzielone przecinkiem lub spacją
#          (np. "10,20", "10 20", "10, 20").
# Działanie: normalizacja separatorów -> walidacja ilości -> konwersja na int -> obliczenia.
# Obsługa błędów:
#  - zła liczba elementów (≠ 2) -> komunikat i ponowna próba,
#  - niepoprawne znaki (np. "a,b") -> ValueError -> komunikat i ponowna próba.
# -----------------------------------------------

# def suma(a, b):
    # Zwykłe dodawanie dwóch liczb. Trzymamy to w osobnej funkcji
    # dla czytelności i ewentualnej rozbudowy w przyszłości.
#    return a + b

# def srednia(lista):
    # Średnia arytmetyczna z elementów listy: suma / liczba elementów.
    # W tym programie lista ma zawsze DOKŁADNIE 2 elementy (po walidacji),
    # więc nie ma ryzyka dzielenia przez zero.
#    return sum(lista) / len(lista)

# while True:
    # 1) Pobranie danych tekstowych od użytkownika.
    #    Od razu NORMALIZUJEMY separatory: spacje zamieniamy na przecinki,
    #    dzięki czemu akceptujemy "10 20" i "10,20" tak samo.
#    raw = input("Podaj dwie liczby oddzielone przecinkami: ").replace(" ", ",")

    # 2) Rozbicie ciągu po przecinku oraz czyszczenie elementów:
    #    - x.strip() usuwa spacje z początku/końca każdego elementu,
    #    - if x.strip() odfiltrowuje ewentualne puste wpisy (np. z "10,,20").
#    parts = [x.strip() for x in raw.split(",") if x.strip()]

    # 3) Walidacja ilości: program oczekuje DOKŁADNIE dwóch wartości.
    #    Jeśli jest inaczej (np. 1 albo 3+), informujemy i wracamy na początek pętli.
#    if len(parts) != 2:
#        print("Dwie liczby! (np. 10,20 lub 10 20)")
#        continue
#    else:
#        try:
            # 4) Konwersja typów w bloku try:
            #    jeżeli użytkownik wpisał literę lub inny nie-liczbowy znak,
            #    int(p) zgłosi ValueError -> przejdziemy do except.
#           nums = [int(p) for p in parts]

#        except ValueError:
            # 5) Obsługa błędu konwersji: prosimy o poprawne liczby i wracamy do inputu.
#            print("Podaj liczby całkowite!")
#            continue
#        else:
            # 6) Jeśli wszystko się udało (brak wyjątków), mamy listę dwóch intów w `nums`.
            #    Teraz możemy policzyć sumę i średnią i zakończyć pętlę.
#            print(f"Suma wprowadzonych liczb: {suma(nums[0], nums[1])}")
#            print(f"Średnia wprowadzonych liczb: {srednia(nums)}")
#            break

# Koniec programu: pętla while True kończy się dzięki 'break' po udanym przetworzeniu danych.
print("="*40)


# 1. Parzysta liczba
# Napisz funkcję, która przyjmuje liczbę i sprawdza, czy jest parzysta.
# Jeśli nie jest parzysta → raise ValueError.
# TODO

def parzysta(x):
    if x % 2 == 0:
        return True
    else:
        raise ValueError("Liczba nieparzysta")
    
try:
    if parzysta(3):
        print("Liczba parzysta.")
except ValueError as e:
    print(e)   
# [OPIS]
# Funkcja parzysta(x) zwraca True dla liczb parzystych,
# a dla nieparzystych rzuca ValueError.
# Przykład pokazuje, że logikę „co zrobić z błędem” trzymamy poza funkcją (try/except).
 


print("="*40)

# 2. Dzielnik
# Funkcja przyjmuje dwie liczby. Zwraca wynik dzielenia.
# Jeśli dzielnik = 0 → raise ZeroDivisionError.
# TODO


def dzielnik(a,b):
    if b == 0:
        raise ZeroDivisionError
    else:
        return a/b

print(dzielnik(2,2))
# [OPIS]
# Funkcja dzielnik(a, b) zgłasza ZeroDivisionError przy b==0 (lub zwraca a/b).
# ZeroDivisionError to „naturalny” wyjątek dla tej sytuacji w Pythonie — spójnie z wbudowanym zachowaniem.



print("="*40)

# 3. Wiek użytkownika
# Funkcja przyjmuje wiek. Jeśli wiek < 0 → raise ValueError.
# Jeśli wiek > 120 → raise ValueError.
# TODO


def age(x):
    if 0 > x or x > 120:
        raise ValueError("Nieprawidłowy wiek")
    return True
    
x = 40    
try:
    if age(x):
        print(f"Niezły wiek, {x} lat!")
except ValueError as e:
    print(e)
# [OPIS]
# Funkcja age(x) waliduje wiek: 0..120 (umowna granica).
# Jeśli poza zakresem — ValueError; przy poprawnym wieku zwraca True.
# Na zewnątrz w try/except wypisujemy przyjazny komunikat użytkownikowi.







print("="*40)

# 4. Lista dodatnich
# Funkcja przyjmuje listę liczb. Sprawdź, czy wszystkie są >= 0.
# Jeśli znajdziesz liczbę ujemną → raise ValueError.
# TODO


numbers = [1,2,3,4,5,-6]

def find_ujemna(numbers):
    for x in numbers:
        if x < 0:
            raise ValueError("Mamy liczbę ujemną w liście")
    return True

try:         
    print(find_ujemna(numbers))
except ValueError as e:
    print(e)
# [OPIS]
# Funkcja find_ujemna(numbers) przechodzi po elementach listy:
# - jeśli trafi na liczbę < 0, rzuca ValueError,
# - jeśli przejdzie całą listę bez błędu, zwraca True.
# Kluczowy detal: 'return True' musi być POZA pętlą, inaczej funkcja zakończy się po 1. elemencie.





print("="*40)

# 5. Odczyt pliku
# Napisz funkcję, która otwiera plik i zwraca jego zawartość.
# Jeśli plik nie istnieje → raise FileNotFoundError.
# Jeśli plik jest pusty → raise ValueError.
# TODO

def file_open(path):    
    with open(path, "r", encoding="utf-8") as f:        
        content = f.read()
        if not content:
            raise ValueError("Plik pusty!")
        return content
    
try:
    text = file_open("../Pliki_i_JSON/pliki_przykladowe/dane.txt")
    print(text)
except FileNotFoundError:
    print("Plik nie istnieje")
except ValueError:
    print("Nie udało się odczytać pliku — brak danych.")
# [OPIS]
# Funkcja file_open(path) otwiera plik, czyta cały tekst i:
# - jeśli plik pusty → ValueError,
# - w przeciwnym razie → zwraca treść.
# Brak pliku (open(..., "r")) zgłosi FileNotFoundError automatycznie — łapiemy go „wyżej”.
# Wzorzec: funkcja ma jedno zadanie (odczyt + walidacja), reakcja jest poza funkcją.



print("="*40)

# 6. Zapis do pliku
# Napisz funkcję, która zapisuje tekst do pliku.
# Jeśli tekst jest pusty → raise ValueError.
# TODO


# ============================================
# 1. Zapis do pliku przy użyciu "".join()
# ============================================

def save_with_join(path, lines):
    """
    Zapisuje listę linijek do pliku jako jeden duży string.
    Każdy element listy musi zawierać znak końca linii \n,
    żeby w pliku były podziały linijek.
    """
    if not lines:   # sprawdzamy, czy lista nie jest pusta
        raise ValueError("Brak danych do zapisania!")

    content = "".join(lines)  # sklejamy listę w jeden string
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)      # zapisujemy cały string na raz


try:
    lines = [
        "Linia pierwsza\n",
        "Linia druga\n",
        "Linia trzecia\n"
    ]
    save_with_join("../Pliki_i_JSON/pliki_przykladowe/zapis_join.txt", lines)
    print("Zapis z join() zakończony sukcesem.")
except ValueError as e:
    print(f"Błąd walidacji: {e}")
except Exception as e:
    print(f"Inny błąd: {e}")



# ============================================
# 2. Zapis do pliku przy użyciu writelines()
# ============================================

def save_with_writelines(path, lines):
    """
    Zapisuje listę linijek do pliku bez sklejania ich w jeden string.
    Funkcja writelines() przyjmuje listę stringów i zapisuje je po kolei.
    """
    if not lines:   # sprawdzamy, czy lista nie jest pusta
        raise ValueError("Brak danych do zapisania!")

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)   # zapis każdej linijki z listy


try:
    lines = [
        "Linia pierwsza\n",
        "Linia druga\n",
        "Linia trzecia\n"
    ]
    save_with_writelines("../Pliki_i_JSON/pliki_przykladowe/zapis_writelines.txt", lines)
    print("Zapis z writelines() zakończony sukcesem.")
except ValueError as e:
    print(f"Błąd walidacji: {e}")
except Exception as e:
    print(f"Inny błąd: {e}")



# ============================================
# 3. Zapis do pliku przy użyciu pętli for
# ============================================

def save_with_loop(path, lines):
    """
    Zapisuje listę linijek do pliku, przechodząc po każdej w pętli.
    Dzięki temu w trakcie zapisu możesz łatwo modyfikować treść
    (np. numerować linie, dodawać prefiksy).
    """
    if not lines:   # sprawdzamy, czy lista nie jest pusta
        raise ValueError("Brak danych do zapisania!")

    with open(path, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line)     # zapis każdej linijki oddzielnie


try:
    lines = [
        "Linia pierwsza\n",
        "Linia druga\n",
        "Linia trzecia\n"
    ]
    save_with_loop("../Pliki_i_JSON/pliki_przykladowe/zapis_loop.txt", lines)
    print("Zapis z pętlą for zakończony sukcesem.")
except ValueError as e:
    print(f"Błąd walidacji: {e}")
except Exception as e:
    print(f"Inny błąd: {e}")
# [OPIS]
# Trzy sposoby zapisu listy linijek do pliku:
# 1) join(): łączymy listę w jeden duży string i zapisujemy jednym write().
# 2) writelines(): przekazujemy listę stringów, zapis idzie po kolei.
# 3) pętla for: pełna kontrola (można numerować, modyfikować).
# Każda funkcja sprawdza pustą listę i rzuca ValueError przy braku danych.
# 'w' tworzy plik, jeśli nie istnieje, lub nadpisuje istniejący.




print("="*40)

# 7. JSON checker
# Funkcja otwiera plik i sprawdza, czy jego zawartość jest poprawnym JSON-em.
# Jeśli nie → raise ValueError.
# (użyj modułu json: json.loads(zawartość))
# TODO

import json

def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

        if not content:
            raise ValueError("Plik jest pusty!")
        
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            raise ValueError("plik nie zawiera poprawnego JSON-a!")
        return data
    
files = [
    "../Pliki_i_JSON/pliki_przykladowe/dane_poprawne.json",
    "../Pliki_i_JSON/pliki_przykladowe/dane_1.json",
    "../Pliki_i_JSON/pliki_przykladowe/tego_pliku_nie_ma.json",
    "../Pliki_i_JSON/pliki_przykladowe/dane_bledne.json"
]


for path in files:
    print(f"\n== Testuję plik: {path} ==")
    
    try:
        result = read_json(path)
        print("OK:", result)
    except FileNotFoundError:
        print("Plik nie istnieje!")
    except ValueError as e:
        print(f"Bład walidacji: {e}")
    print()
# [OPIS]
# read_json(path) czyta tekst pliku i:
# - jeśli pusty → ValueError("Plik jest pusty!"),
# - jeśli nieprawidłowy JSON → łapie json.JSONDecodeError i rzuca ValueError z czytelnym komunikatem,
# - jeśli OK → zwraca sparsowane dane (dict/list).
# Pętla testów przechodzi po kilku ścieżkach: poprawny, brak pliku, pusty, błędny JSON.
# Dzięki oddzielnym exceptom masz czytelne komunikaty dla użytkownika.




print("="*40)

# 8. Otwórz i policz linie
# Funkcja otwiera plik i zwraca liczbę linii.
# Jeśli plik jest pusty → raise ValueError.
# TODO

def count_lines(path):
    with open(path, "r", encoding="utf-8") as f:
        line = f.readlines()       
        if not line:
            raise ValueError("Plik pusty")
        return len(line)

print(count_lines("../Pliki_i_JSON/pliki_przykladowe/zapis_loop.txt"))
# [OPIS]
# count_lines(path) używa readlines() do wczytania wszystkich wierszy:
# - jeśli lista jest pusta → ValueError("Plik pusty"),
# - w przeciwnym razie → zwraca liczbę linii (len(listy)).
# Uwaga: dla bardzo dużych plików można użyć pamięciooszczędnego sum(1 for _ in f).




print("="*40)

# 9. Kalkulator
# Funkcja przyjmuje operator (+, -, *, /) i dwie liczby.
# Jeśli operator nie jest jednym z dozwolonych → raise ValueError.
# TODO

def calculate(operator, a, b):
    if operator not in ["+", "-", "*", "/"]:
        raise ValueError("Niepoprawny operator!")
    if operator == "+":
        return a + b
    if operator == "-":
        return a - b
    if operator == "*":
        return a * b
    if operator == "/":
        return a / b
    
try:
    print(f"Dodawanie 5,5: {calculate("+", 5,5)}")
    print(f"Mnożenie 5,5: {calculate("*", 5,5)}")
    print(f"Odejmowanie 5,5: {calculate("-", 5,5)}")
    print(f"Dzielenie 5,5: {calculate("/", 5,5)}")
except ValueError as e:
    print(f"Błąd: {e}")
# [OPIS]
# calculate(operator, a, b) obsługuje cztery operacje: +, -, *, /.
# - Jeśli operator spoza listy dozwolonych → ValueError.
# - Przy dzieleniu warto pamiętać o dzieleniu przez 0 (tu celowo pominięte — ćwiczenie).
# Wypisy w f-stringach wymagają poprawnej składni cudzysłowów:
#   {calculate('+', 5, 5)} zamiast {calculate("+", 5, 5)} wewnątrz f"..."




print("="*40)

# 10. Rejestr użytkownika
# Funkcja przyjmuje słownik {"name": ..., "age": ...}.
# Jeśli nie ma klucza "name" → raise KeyError.
# Jeśli age < 0 → raise ValueError.
# TODO



def user_data(data):    
        if "name" not in data:
            raise KeyError("Brak klucza")
        elif data.get("age", 0) < 0:
            raise ValueError("Wiek nie może być ujemny")
        return data

dict_data = {"name": "Robert", "age": 43, "city": "Poznań" }

try:
    print(user_data(dict_data))
except (ValueError, KeyError) as e:
    print(f"Bład: {e}")
# [OPIS]
# user_data(data) waliduje słownik z danymi użytkownika:
# - jeśli brak klucza 'name' → KeyError (zgodnie ze specyfikacją zadania),
# - jeśli 'age' < 0 → ValueError,
# - przy sukcesie zwraca oryginalny słownik (do dalszego użycia).
# W bloku try/except łapiemy oba wyjątki i wypisujemy czytelną informację.




print("="*40)

