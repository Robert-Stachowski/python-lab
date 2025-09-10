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


try:
    with open("config.json", "r", encoding="utf-8") as file:
        data = file.read()
except FileNotFoundError:
    print("Błąd! Nie znaleziono pliku!")
    data = {"theme": "light", "lang": "pl"}
except PermissionError:
    print("Bład! Brak uprawnien do odczytu pliku")
    data = {"theme": "light", "lang": "pl"}
else:
    print("Wszytsko ok")
finally:
    print("Koniec próby wczytania konfiguracji")









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



print("="*40)

# 5. Odczyt pliku
# Napisz funkcję, która otwiera plik i zwraca jego zawartość.
# Jeśli plik nie istnieje → raise FileNotFoundError.
# Jeśli plik jest pusty → raise ValueError.
# TODO

print("="*40)

# 6. Zapis do pliku
# Napisz funkcję, która zapisuje tekst do pliku.
# Jeśli tekst jest pusty → raise ValueError.
# TODO

print("="*40)

# 7. JSON checker
# Funkcja otwiera plik i sprawdza, czy jego zawartość jest poprawnym JSON-em.
# Jeśli nie → raise ValueError.
# (użyj modułu json: json.loads(zawartość))
# TODO

print("="*40)

# 8. Otwórz i policz linie
# Funkcja otwiera plik i zwraca liczbę linii.
# Jeśli plik jest pusty → raise ValueError.
# TODO

print("="*40)

# 9. Kalkulator
# Funkcja przyjmuje operator (+, -, *, /) i dwie liczby.
# Jeśli operator nie jest jednym z dozwolonych → raise ValueError.
# TODO

print("="*40)

# 10. Rejestr użytkownika
# Funkcja przyjmuje słownik {"name": ..., "age": ...}.
# Jeśli nie ma klucza "name" → raise KeyError.
# Jeśli age < 0 → raise ValueError.
# TODO

print("="*40)

