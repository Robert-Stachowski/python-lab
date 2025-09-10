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
    try:
        liczby = [int(x.strip()) for x in input("Podaj dwie liczby oddzielone przecinkami: ").split(",")]
    except ValueError:
        print("Podaj liczby!")
        continue
    else:
        print(f"Suma wprowadzonych liczb: {suma(liczby[0], liczby[1])}")
        print(f"Średnia wprowadzonych liczb: {srednia(liczby)}")








print("="*40)
print("5. API – symulacja timeoutu")
# Opis: Zasymuluj funkcję fetch(), która czasem rzuca TimeoutError. Obsłuż ją z retry=1.
# TODO: try/except TimeoutError, jeśli błąd -> jedna ponowna próba, potem komunikat.