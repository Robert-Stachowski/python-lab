# =========================================================
# 1. ZAPIS I ODCZYT PLIKU
# Napisz funkcję save_note(text), która zapisze tekst do pliku "note.txt".
# Potem napisz funkcję read_note(), która odczyta zawartość pliku i zwróci stringa.
# Obsłuż przypadek, gdy pliku nie ma (FileNotFoundError).
# TODO

def save_note(path, data):
    if not data:
            raise ValueError("Brak treści")
    with open(path, "w", encoding="utf-8") as f:
        f.write(data)
        
        
def read_note(path):    
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if not content:
        raise ValueError("Błąd, brak treści")
    return content  


text = "To jest przykładowy tekst dla funkcji save_note()"
try:
    print("\nPlik zapisano!\n")
    save_note(r"Files_samples\note.txt", text)
    print("Plik odczytano:")
    print(read_note(r"Files_samples\note.txt"))
    print("\n")
except FileNotFoundError:
    print("Nie znaleziono pliku")
except ValueError as e:
    print(f"Wystąpił błąd: {e}")
except Exception as e:
    print(f"Wystąpił nieoczekiwany błąd: {e}")

# =========================================================
# ---


# =========================================================
# 2. TRY/EXCEPT NA INPUT
# Użytkownik podaje dwie liczby rozdzielone przecinkiem.
# Napisz program, który obliczy ich sumę i średnią.
# Obsłuż błędy: nieprawidłowe dane (ValueError), dzielenie przez zero.
# TODO


while True:  # pętla nieskończona – program działa aż użytkownik wpisze poprawne dane
    try:
        # input() zwraca string, np. "10, 20"
        # split(",") → ["10", " 20"]
        # x.strip() → usuwa spacje
        # int(x.strip()) → zamienia string na liczbę całkowitą
        # comprehension → lista intów, np. [10, 20]
        y = [int(x.strip()) for x in input("Podaj dwie liczby oddzielone przecinkami: ").split(",")]

        # sprawdzamy, czy użytkownik podał dokładnie 2 liczby
        if len(y) != 2:
            # jeśli nie – zgłaszamy wyjątek (skok do except)
            raise ValueError("Podaj dokładnie dwie liczby")

        # jeśli dane poprawne:
        srednia = sum(y) / len(y)  # średnia = suma elementów / ilość elementów
        print(f"Średnia: {srednia}")
        print(f"Suma: {sum(y)}")
        break  # wychodzimy z pętli, bo dane były poprawne

    except ValueError as e:
        # przechwycenie błędów: literówki, zła ilość elementów, błędna konwersja
        print(f"Błąd: {e}")
        continue  # wracamy na początek pętli i pytamy użytkownika jeszcze raz
print(40* "=")

# =========================================================
# 2. TRY/EXCEPT NA INPUT – wersja funkcyjna
#
# Cel:
# - Użytkownik podaje dwie liczby rozdzielone przecinkiem.
# - Program liczy sumę i średnią.
# - Obsługujemy błędy: złe dane (ValueError), zła ilość argumentów.
#
# Struktura:
# 1. get_input() → zajmuje się tylko inputem i walidacją.
# 2. add(a, b), avg(a, b) → czyste funkcje matematyczne.
# 3. logika główna → korzysta z tych funkcji.
# =========================================================
#def get_input():
"""
    Funkcja pyta użytkownika o dwie liczby.
    - Używa pętli while True → powtarza się aż dane będą poprawne.
    - Jeśli użytkownik poda złe dane → ValueError i wracamy do pytania.
    - Jeśli poprawne → zwraca listę [a, b] (dwie liczby całkowite).
    """
#    while True:
#        try:
            # input() → pobiera dane jako string, np. "10, 20"
#            parts = input("Podaj dwie liczby oddzielone przecinkami: ").split(",")

            # konwersja na int, z usunięciem spacji
#            nums = [int(x.strip()) for x in parts]

            # walidacja ilości elementów
#            if len(nums) != 2:
#                raise ValueError("Podaj dokładnie dwie liczby")

#            return nums  # jeśli wszystko OK → wychodzimy z funkcji

#        except ValueError as e:
#            # obsługa błędów: złe znaki, zła ilość danych
#            print(f"Błąd: {e}")
#            continue  # wracamy do początku pętli


#def add(a, b):
#    """Zwraca sumę dwóch liczb."""
#    return a + b


# def avg(a, b):
#    """Zwraca średnią dwóch liczb."""
#    return (a + b) / 2

# =========================================================
# Główna logika programu
# =========================================================

# Pobieramy dane od użytkownika przez naszą funkcję get_input()
# numbers = get_input()

# Rozpakowujemy listę [a, b] → do osobnych argumentów w funkcjach add i avg
# print(f"Suma: {add(*numbers)}")
# print(f"Średnia: {avg(*numbers)}")
# UWAGA: operator * rozpakowuje listę na argumenty funkcji.
# numbers = [10, 20]
# add(*numbers) → add(10, 20)
# avg(*numbers) → avg(10, 20)
# Bez gwiazdki byłoby add([10, 20]) → błąd (funkcja oczekuje 2 liczb, nie jednej listy).


# =========================================================
# ---





# =========================================================
# 3. FUNKCJA I HISTORIA DZIAŁAŃ
# Napisz funkcję calc_sum(a, b), która zwraca sumę.
# Każde wywołanie zapisz w liście history (np. "2+3=5").
# Na końcu wydrukuj całą historię działań.
# TODO

class History_calc:
    def __init__(self):
        self.history = []

    def show_history(self):
        if not self.history:
            print("Historia pusta")
        print("Historia operacji: ")
        for entry in self.history:
            print(entry)
        
    def calc_sum(self, a,b):
        result = a+b   
        self.history.append(f"{a} + {b} = {result}")     
        return result
        

calc = History_calc()
while True:
    
    try:
        raw_input = input("Podaj dwie liczby oddzielone przecinkami: ").split(",")
        nums = [int(q.strip()) for q in raw_input]

        if len(nums) != 2:
            raise ValueError("Błąd, podaj dokładnie dwie liczby")
        
        print(calc.calc_sum(*nums))
        calc.show_history()
        break

    except ValueError as e:
        print(f"Bład: {e}")
        continue
print(40* "=")

# =========================================================
# 3. FUNKCJA I HISTORIA DZIAŁAŃ – KOMENTARZE
#
# Wersja 1: obiektowa (klasa History_calc)
# ---------------------------------------
# - Tworzymy klasę History_calc.
# - Konstruktor __init__ zakłada pustą listę self.history.
# - Metoda calc_sum(a, b) liczy sumę i zapisuje do historii
#   w formie stringa: "a + b = wynik".
# - Metoda show_history() drukuje historię wszystkich operacji.
#
# Zalety podejścia obiektowego:
# - Historia działań "żyje" wewnątrz obiektu → nie ma globalnych zmiennych.
# - Można stworzyć kilka niezależnych kalkulatorów z własną historią.
# - Bardziej zbliżone do pracy w Django/większych projektach (OOP).
#
# Wersja 2: proceduralna (funkcja + lista history)
# ------------------------------------------------
# - Zamiast klasy używamy jednej listy history = [].
# - Funkcja calc_sum(a, b, history) liczy sumę i dokleja wpis do listy.
# - Historia jest zwykłą listą, którą drukujemy na końcu.
#
# Zalety podejścia proceduralnego:
# - Prostsze → mniej kodu, łatwiej ogarnąć na start.
# - Wystarczy, gdy robisz szybki skrypt lub ćwiczenie.
#
# ---------------------------------------------------------
# PRZYKŁAD – WERSJA PROCEDURALNA (alternatywa do klasy):
#
# history = []
#
# def calc_sum(a, b, history):
#     result = a + b
#     history.append(f"{a} + {b} = {result}")
#     return result
#
# # użycie
# print(calc_sum(2, 3, history))
# print(calc_sum(10, 5, history))
# print("Historia:", history)
#
# Wynik działania:
# 5
# 15
# Historia: ['2 + 3 = 5', '10 + 5 = 15']
# ---------------------------------------------------------
# =========================================================
# ---





# =========================================================
# 4. LIST COMPREHENSION
# Masz listę liczb 1–20. Zbuduj nową listę zawierającą tylko kwadraty liczb parzystych.
# Użyj list comprehension.
# TODO

lista = [2,3,6,5,8,9,62,31,23,33]
square_list = [x**2 for x in lista if x % 2 == 0]
print(f"Lista: {lista}")
print(f"Kwadraty listy liczb parzystych: {square_list}")
print(40* "=")

# =========================================================

# ---


# =========================================================
# 5. SLICING
# Masz listę 10 liczb [0..9].
# 1) Wyświetl elementy od indeksu 2 do 6.
# 2) Wyświetl co drugi element.
# 3) Odwróć całą listę.
# TODO

lista = [0,1,2,3,4,5,6,7,8,9]
print(lista[2:7])
print(lista[::2])
print(lista[::-1])
print(40* "=")
# =========================================================

# ---


# =========================================================
# 6. WBUILT MODULE – RANDOM
# Wylosuj 5 liczb z przedziału 1–100.
# Zapisz je do pliku "randoms.txt".
# Potem odczytaj plik i policz średnią.
# TODO
import random

def write_random_nums(length):
    nums = [random.randint(1,100) for _ in range(length)]    
    with open(r"Files_samples\randoms.txt", "w", encoding="utf-8")as f:
        f.write(", ".join(str(x) for x in nums))
    return nums

def read_random_nums():    
    with open(r"Files_samples\randoms.txt", "r", encoding="utf-8")as f:
        content = f.read()
    if not content:
        raise ValueError("Pusty plik")
    nums_from_file = [int(x.strip())for x in content.split(",")]
    return nums_from_file


length = 5
print("Zapis:")
print(write_random_nums(length))

print("Odczyt:")
numbers = read_random_nums()
print(numbers)

avr_num = sum(numbers) / len(numbers)
print("Średnia:")
print(avr_num)
print(40* "=")

# =========================================================

# ---


# =========================================================
# 7. FUNKCJA + TRY/EXCEPT
# Napisz funkcję divide(a, b), która zwraca wynik dzielenia.
# Jeśli b = 0 → raise ValueError.
# Obsłuż wyjątek w kodzie głównym i wypisz komunikat.
# TODO

def divide(a, b):
    if b == 0:
        raise ValueError("Błąd, dzielenie przez zero")
    return a / b

try:
    print(divide(3,2))
except ValueError as e:
    print(f"Wystąpił błąd: {e}")

print(40* "=")


# =========================================================     
# ---


# =========================================================
# 8. SET/DICT COMPREHENSION
# Masz listę słów: ["kot", "pies", "kot", "mysz", "pies"].
# Utwórz słownik {słowo: liczba_wystąpień} za pomocą dict comprehension.
# TODO
from collections import Counter


lista = ["kot", "pies", "kot", "mysz", "pies"]
#lista_dict = Counter(lista)
lista_dict = {word: lista.count(word) for word in set(lista)}
print(lista_dict)
print(40* "=")

# ---------------------------------------------------------
# 1) Używamy dict comprehension, czyli słownika tworzonego
#    w jednej linijce.
#
# 2) Konstrukcja:
#    {klucz: wartość for element in kolekcja}
#
# 3) W naszym przypadku:
#    - klucz → słowo (word)
#    - wartość → ile razy to słowo występuje w liście
#      (lista.count(word))
#    - kolekcja → set(lista), czyli zbiór unikalnych słów
#
# Dlaczego set(lista)?
# - Gdybyśmy iterowali po całej liście, to liczenie
#   powtarzałoby się dla każdego wystąpienia (np. "kot"
#   byłby liczony dwa razy). 
# - Zbiór (set) usuwa duplikaty, więc każde słowo liczymy raz.
#
# ---------------------------------------------------------
# Alternatywy:
# - Można by użyć Counter(lista) z modułu collections,
#   który daje to samo szybciej i wygodniej.
# - Ale tu ćwiczymy comprehension, więc robimy "na piechotę".
#
# =========================================================









# =========================================================
# 9. MODUŁ WBUILT – JSON
# Utwórz słownik {"user": "Robert", "level": "junior"}.
# Zapisz go jako config.json.
# Odczytaj plik i wyświetl dane.
# Obsłuż błąd pustego pliku.
# TODO
import json


def json_write_data(path, data):
    if not data:
        raise ValueError("Brak danych do zapisu")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def json_read_data(path):
    with open(path, "r", encoding="utf-8") as f:
        content = json.load(f)
        if not content:
            raise ValueError("Plik pusty")
        return content





config_2 = {"user": "Robert", "level": "junior"}

try:
    print("Plik config_2.json zapisano")
    json_write_data(r"Files_samples\config_2.json", config_2)
    output_data = json_read_data(r"Files_samples\config_2.json")
    print(output_data)

except ValueError as e:
    print(f"Wykryto błąd: {e}")
except FileNotFoundError:
    print("Pliku nie znaleziono")





# =========================================================

# ---


# =========================================================
# 10. MINI PROJEKT – HISTORIA DZIAŁAŃ Z PLIKIEM
# Napisz prosty kalkulator w pętli while True:
# - użytkownik podaje działanie w formie "a+b" lub "a-b".
# - program liczy wynik i wyświetla.
# - każde działanie dopisuje do pliku "history.txt".
# - komenda "quit" kończy program.
# Obsłuż błędy: złe dane, brak pliku, ValueError.
# TODO

class Calculate:
    def __init__(self):
        self.history = []

    def show_history(self):
        if not self.history:
            print("Historia pusta")
            return
        print("Historia operacji: ")
        for entry in self.history:
            print(entry)    
    
    def add(self, a, b):
        return a+b
    
    def subtract(self, a, b):
        return a-b
    
    def multiply(self, a, b):
        return a*b
    
    def power(self, a, b):
        return a**b
    
    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Nie można dzielić przez zero")
        return a/b

    def calc_map(self, a, b, operation):
        operating_map = {
            "a+b": self.add,
            "a-b": self.subtract,
            "a*b": self.multiply,
            "a**b": self.power,
            "a/b": self.divide
        }
        func = operating_map[operation]
        result = func(a,b)
        entry = f"{a} {operation[1:-1]} {b} = {result}"
        self.history.append(entry)
        with open(r"Files_samples\history.txt", "a", encoding="utf-8") as f:
            f.write(entry+ "\n")
        return result
    
calc = Calculate()

while True:
    operation = input("Podaj operację typu: a+b, a-b itd dla kalkulatora lub exit dla wyjścia: ")
    allowed_operation = ["a+b","a-b","a*b","a**b","a/b"]

    if operation == "exit":
        calc.show_history()
        break

    if operation not in allowed_operation:
        print("Nieznana operacja, try again :) ")
        continue

    try:
        numbers_text = input("Podaj liczby ( a i b) oddzielone przecinkami: ").split(",")
        nums = [int(x.strip())for x in numbers_text]
        if len(nums) != 2:
            raise ValueError("Bład, podaj dokładnie dwie liczby!")
        result = calc.calc_map(*nums, operation)
        print(result)

    except ValueError as e:
        print(f"Wystąpił błąd: {e}")
    except ZeroDivisionError as e:
        print(f"Błąd: {e}")
    except KeyboardInterrupt:
        print("\nPrzerwano program klawiszem.")
        break



# =========================================================
