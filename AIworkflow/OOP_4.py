"""
**Zadanie**:  
Stwórz klasę `Car`, która przechowuje:
- markę (`brand`)
- model (`model`)
- rok produkcji (`year`)

Dodaj metodę `info()`, która zwraca tekst w stylu:  
`"Toyota Corolla, rocznik 2020"`
"""
# Definicja klasy Car, która reprezentuje samochód
class Car:
    # Konstruktor __init__ przyjmuje 3 argumenty: markę, model i rok produkcji
    def __init__(self, brand, model, year):
        # Przypisujemy wartości do atrybutów obiektu
        self.brand = brand
        self.model = model
        self.year = year

    # Metoda info() zwraca sformatowany tekst z danymi samochodu
    def info(self):
        return f"{self.brand} {self.model} rocznik {self.year}"

# Tworzymy obiekt klasy Car z konkretnymi danymi
cars = Car("toyota", "corolla", 2020)

# Wywołujemy metodę info() i wypisujemy wynik
print(cars.info())

"""
---

## 🧪 Ćwiczenie 2: Klasa `Student`

**Zadanie**:  
Stwórz klasę `Student`, która przechowuje:
- imię (`name`)
- wiek (`age`)
- listę ocen (`grades`)

Dodaj metodę `average()`, która zwraca średnią ocen.
"""

# Definicja klasy Student, która przechowuje dane ucznia
class Student:
    # Konstruktor przyjmuje imię, wiek i listę ocen
    def __init__(self, name, age, grades):
        self.name = name
        self.age = age
        self.grades = grades

    # Metoda average() oblicza średnią ocen
    def average(self):
        # Jeśli lista ocen jest pusta, zwracamy komunikat
        if not self.grades:
            return "Brak ocen"
        # Obliczamy średnią jako suma ocen podzielona przez ich liczbę
        return sum(self.grades) / len(self.grades)

    # Metoda __str__ pozwala na czytelne wypisanie obiektu przez print()
    def __str__(self):
        return f"{self.name} ma średnią z ocen: {self.average()}"

# Tworzymy obiekt klasy Student z przykładowymi danymi
student = Student("Michał", 23, [3, 4, 3, 3, 5, 6])

# Wypisujemy obiekt — automatycznie wywoła __str__()
print(student)
            
"""
## 🧪 Ćwiczenie 1: Klasa `Converter`

**Zadanie**:  
Stwórz klasę `Converter`, która zawiera dwie metody:
- `km_to_miles(km)` — zamienia kilometry na mile (1 km ≈ 0.621371 mi)
- `celsius_to_fahrenheit(c)` — zamienia stopnie Celsjusza na Fahrenheita

Nie twórz konstruktora `__init__`. Użyj klasy bez tworzenia obiektu.
"""
# Definicja klasy Converter — zestaw narzędzi bez konstruktora
class Converter:
    # Metoda zamieniająca kilometry na mile
    def km_to_miles(a):
        return round((a * 0.621371), 2)

    # Metoda zamieniająca stopnie Celsjusza na Fahrenheita
    def cel_to_faren(c):
        return (c * 1.8) + 32

# Wywołujemy metody bez tworzenia obiektu — bo nie ma __init__
print(Converter.km_to_miles(60))     # 60 km → mile
print(Converter.cel_to_faren(30))    # 30°C → °F



"""
## 🧪 Ćwiczenie 2: Klasa `TextTools`

**Zadanie**:  
Stwórz klasę `TextTools`, która zawiera dwie metody:
- `count_words(text)` — zwraca liczbę słów w tekście
- `is_palindrome(text)` — zwraca `True`, jeśli tekst jest palindromem (ignorując wielkość liter i spacje)

Nie używaj `__init__`. Użyj klasy jako zestawu narzędzi — bez tworzenia obiektu.
"""

# Definicja klasy TextTools — zestaw narzędzi tekstowych
class TextTools:
    # Metoda licząca słowa w tekście
    def count_words(text):
        if not text:
            return "Błąd, tekst pusty"
        # Dzielimy tekst po spacjach i liczymy elementy
        words = text.split()
        return len(words)

    # Metoda sprawdzająca, czy tekst jest palindromem
    def is_palindrome(text):
        if not text:
            return "Błąd, brak tekstu"
        # Usuwamy spacje i zamieniamy na małe litery
        cleaned = text.replace(" ", "").lower()
        # Porównujemy tekst z jego odbiciem
        return cleaned == cleaned[::-1]

# Testujemy metody klasy bez tworzenia obiektu
print(TextTools.count_words("mucha nasrała na łyżeczkę"))  # Liczy słowa
print(TextTools.is_palindrome("a to idiota"))              # Sprawdza palindrom

"""
## 🧪 Ćwiczenie 1: Klasa `Geometry`

**Zadanie**:  
Stwórz klasę `Geometry`, która zawiera dwie metody:
- `rectangle_area(width, height)` — zwraca pole prostokąta
- `triangle_area(base, height)` — zwraca pole trójkąta (wzór: ½ × podstawa × wysokość)

Nie używaj `__init__`. Użyj klasy bez tworzenia obiektu.
"""
# Definicja klasy Geometry — zestaw narzędzi matematycznych
# Nie używamy __init__, bo nie przechowujemy żadnych danych — tylko metody
class Geometry:
    # Metoda obliczająca pole prostokąta
    def rectangle_area(width, height):
        return width * height

    # Metoda obliczająca pole trójkąta (0.5 × podstawa × wysokość)
    def triangle_area(w, b):
        return 0.5 * w * b

# Wywołujemy metody bez tworzenia obiektu — bo nie ma konstruktora
print(Geometry.rectangle_area(10, 5))  # Pole prostokąta: 10×5 = 50
print(Geometry.triangle_area(10, 5))   # Pole trójkąta: 0.5×10×5 = 25.0
"""
## 🧪 Ćwiczenie 2: Klasa `StringTools`

**Zadanie**:  
Stwórz klasę `StringTools`, która zawiera dwie metody:
- `reverse(text)` — zwraca odwrócony tekst
- `shout(text)` — zwraca tekst pisany wielkimi literami z wykrzyknikiem na końcu

Nie używaj `__init__`. Użyj klasy jako zestawu narzędzi — bez tworzenia obiektu.
"""

# Klasa StringTools — zestaw narzędzi tekstowych
# Nie używamy __init__, bo nie przechowujemy danych — tylko operujemy na argumentach
class StringTools:
    # Metoda reverse — odwraca tekst (np. "abc" → "cba")
    def reverse(text):
        return text[::-1]

    # Metoda shout — zamienia tekst na wielkie litery i dodaje wykrzyknik
    def shout(text):
        return f"{text.upper()}!"

# Testujemy metody bez tworzenia obiektu
print(StringTools.reverse("Dzień dobry"))  # → "yrbod ńeizD"
print(StringTools.shout("Dzień dobry"))    # → "DZIEŃ DOBRY!"

# ============================================
# 🧠 ĆWICZENIA Z DZIEDZICZENIA — JUNIOR LEVEL
# ============================================

# Ćwiczenie 1: Proste dziedziczenie bez __init__
# ------------------------------------------------
# Stwórz klasę Shape z metodą describe() zwracającą "To jest figura geometryczna."
# Stwórz klasę Circle, która dziedziczy po Shape.
# Utwórz obiekt Circle i wywołaj metodę describe().

# Klasa bazowa Shape — zawiera metodę describe()
class Shape:
    def describe(self):
        return "To jest figura geometryczna"

# Klasa Circle dziedziczy po Shape
# Nie dodaje nowych metod, tylko wywołuje metodę bazową przez super()
class Circle(Shape):
    def describe(self):
        return super().describe()

# Tworzymy obiekt klasy Circle i wywołujemy odziedziczoną metodę
obj = Circle()
print(obj.describe())  # → "To jest figura geometryczna"


# Ćwiczenie 2: Dziedziczenie z __init__ bez nadpisywania
# -------------------------------------------------------
# Stwórz klasę User z __init__(name) i metodą greet() zwracającą "Witaj, {name}!"
# Stwórz klasę Admin, która dziedziczy po User, ale nie nadpisuje __init__.
# Utwórz obiekt Admin("Robert") i wywołaj greet().

# Klasa bazowa User — przechowuje imię i ma metodę greet()
class User:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Witaj {self.name}!"

# Klasa Admin dziedziczy po User
# Nie nadpisuje __init__, więc korzysta z wersji bazowej
# Nadpisuje greet(), ale używa super() do rozszerzenia komunikatu
class Admin(User):
    def greet(self):
        return super().greet() + " Masz dostęp do panelu administratora."

# Tworzymy obiekt klasy Admin i wywołujemy greet()
obj = Admin("Robert")
print(obj.greet())  # → "Witaj Robert! Masz dostęp do panelu administratora."




# Ćwiczenie 3: Dziedziczenie z nadpisaniem __init__ i użyciem super()
# --------------------------------------------------------------------
# Stwórz klasę Vehicle z __init__(brand) i metodą info() zwracającą "Marka: {brand}"
# Stwórz klasę Car, która dziedziczy po Vehicle, dodaje model i nadpisuje __init__ z użyciem super()
# Dodaj metodę full_info() zwracającą "Marka: {brand}, Model: {model}"

# Klasa bazowa Vehicle — przechowuje markę pojazdu
class Vehicle:
    def __init__(self, brand):
        self.brand = brand

    # Metoda info() zwraca tekst z marką pojazdu
    def info(self):
        return f"Marka: {self.brand}"

# Klasa Car dziedziczy po Vehicle
# Dodaje nowy atrybut: model
# Nadpisuje konstruktor __init__, ale używa super() do inicjalizacji brand
class Car(Vehicle):
    def __init__(self, brand, model):
        super().__init__(brand)  # wywołanie konstruktora klasy bazowej
        self.model = model       # dodanie nowego atrybutu

    # Metoda full_info() łączy info() z klasy bazowej i dodaje model
    def full_info(self):
        return super().info() + f" , Model: {self.model}"

# Tworzymy obiekt klasy Car i wypisujemy pełne informacje
obj = Car("Toyota", "Corolla")
print(obj.full_info())  # → "Marka: Toyota , Model: Corolla"



# Ćwiczenie 4: Nadpisywanie metody z użyciem super()
# ---------------------------------------------------
# Stwórz klasę Printer z metodą print_message() wypisującą "Drukuję wiadomość..."
# Stwórz klasę ColorPrinter, która dziedziczy po Printer i nadpisuje print_message()
# W nowej wersji najpierw wywołaj super().print_message(), a potem dodaj "...w kolorze!"

# Klasa bazowa Printer — zawiera metodę print_message()
class Printer:
    def print_message(self):
        return "Drukuję wiadomość..."

# Klasa ColorPrinter dziedziczy po Printer
# Nadpisuje metodę print_message(), ale używa super() do rozszerzenia komunikatu
class ColorPrinter(Printer):
    def print_message(self):
        return super().print_message() + " ... w kolorze!"

# Tworzymy obiekt klasy ColorPrinter i wywołujemy metodę
print(ColorPrinter().print_message())  # → "Drukuję wiadomość... ... w kolorze!"




# Ćwiczenie 5: Dziedziczenie wielopoziomowe
# -----------------------------------------
# Stwórz klasę LivingBeing z metodą exist() zwracającą "Istnieję"
# Stwórz klasę Animal, która dziedziczy po LivingBeing
# Stwórz klasę Dog, która dziedziczy po Animal
# Utwórz obiekt Dog() i wywołaj exist()

# Klasa bazowa LivingBeing — zawiera metodę exist()
class LivingBeing:
    def exist(self):
        return "Istnieję..."

# Klasa Animal dziedziczy po LivingBeing
class Animal(LivingBeing):
    def exist(self):
        return super().exist()

# Klasa Dog dziedziczy po Animal
class Dog(Animal):
    def exist(self):
        return super().exist()

# Tworzymy obiekt klasy Dog i wywołujemy metodę exist()
obj = Dog()
print(obj.exist())  # → "Istnieję..."


# ============================================
# 🧪 ĆWICZENIE: Świadome użycie super() w metodzie
# ============================================

# Zadanie:
# Stwórz klasę BaseValidator z metodą validate(data),
# która sprawdza, czy data nie jest pusta i zwraca "OK" lub "Brak danych".

# Następnie stwórz klasę LengthValidator, która dziedziczy po BaseValidator
# i nadpisuje metodę validate(data), aby:
# - najpierw wywołać super().validate(data)
# - jeśli wynik to "Brak danych", zwrócić go od razu
# - jeśli wynik to "OK", sprawdzić czy długość data > 5
# - jeśli tak, zwrócić "Dane poprawne"
# - jeśli nie, zwrócić "Za krótki tekst"

# Przykład użycia:
# obj = LengthValidator()
# print(obj.validate("abc"))       # Za krótki tekst
# print(obj.validate(""))          # Brak danych
# print(obj.validate("abcdef"))    # Dane poprawne


# Klasa bazowa BaseValidator — sprawdza, czy dane nie są puste
class BaseValidator:
    def validate(self, data):
        self.data = data
        if not data:
            return "Brak danych"
        return "OK"

# Klasa LengthValidator dziedziczy po BaseValidator
# Nadpisuje metodę validate(), ale używa super() do wstępnej walidacji
class LenghtValidator(BaseValidator):
    def validate(self, data):
        result = super().validate(data)  # wywołanie walidacji bazowej

        if result == "Brak danych":
            return result  # jeśli dane puste, zwracamy od razu
        elif len(data) > 5:
            return "Dane poprawne"  # jeśli długość > 5, dane są OK
        else:
            return "Za krótki tekst"  # w przeciwnym razie komunikat o błędzie

# Testujemy klasę LengthValidator z różnymi danymi
obj = LenghtValidator()
print(obj.validate("aaa"))      # → "Za krótki tekst"
print(obj.validate(""))         # → "Brak danych"
print(obj.validate("abcdef"))   # → "Dane poprawne"


# ============================================
# 
# ============================================


"""
Stwórz klasę Shape z metodą area(), która zwraca "Brak wzoru"
Stwórz klasy Circle i Rectangle, które nadpisują area() i zwracają odpowiednie obliczenia.
Utwórz listę obiektów i wypisz ich pole powierzchni w pętli.

"""
import math

# Klasa bazowa Shape — definiuje wspólny interfejs dla figur geometrycznych
class Shape:
    # Metoda area() zwraca domyślny komunikat — brak wzoru
    def area(self):
        return "Brak wzoru"

# Klasa Circle dziedziczy po Shape i dodaje promień
class Circle(Shape):
    def __init__(self, r):
        self.r = r

    # Nadpisujemy metodę area() — obliczamy pole koła
    def area(self):
        return round((math.pi * self.r * self.r), 2)

# Klasa Rectangle dziedziczy po Shape i dodaje długości boków
class Rectangle(Shape):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    # Nadpisujemy metodę area() — obliczamy pole prostokąta
    def area(self):
        return self.a * self.b

# Tworzymy listę obiektów różnych klas — pokazujemy polimorfizm
obj = [Shape(), Circle(12), Rectangle(2, 6)]

# W pętli wywołujemy area() — każdy obiekt zachowuje się zgodnie ze swoją klasą
for x in obj:
    print(x.area())


# ============================================
# 🧪 MINI CRM — ROZGRZEWKA
# ============================================

# Stwórz klasę User z __init__(name, email) i metodą view_data()
# która zwraca "Dane użytkownika: {name}, {email}"

# Stwórz klasę Admin, która dziedziczy po User i nadpisuje view_data()
# tak, aby zwracała "Panel administratora: {name}, {email}"

# Stwórz klasę Client, która dziedziczy po User i nadpisuje view_data()
# tak, aby zwracała "Klient: {name}"

# Utwórz listę obiektów: [Admin("Robert", "admin@crm.pl"), Client("Anna", "anna@crm.pl")]
# Wypisz dane każdego użytkownika w pętli, wywołując view_data()

class User:
    def __init__(self,name, email):
        self.name = name
        self.email = email

    def view_data(self):
        return f"Dane użytkownika: {self.name}, {self.email}"
    
class Admin(User):
    def __init__(self, name, email):
        super().__init__(name, email)
        
    
    def edit_profile(self,new_name, new_email):  
        self.new_name= new_name
        self.new_email = new_email
        self.name = self.new_name
        self.email = self.new_email
        return self.name, self.email

    def view_data(self):
        return f"Panel Administratora: {self.name}, {self.email}"

class Client(User):
    def __init__(self, name, email):
        super().__init__(name,email)
        
    def edit_profile(self, new_name):
            self.new_name = new_name
            self.name = self.new_name
            return self.name

    def view_data(self):
        return f"Klient: {self.name}"
    
class CRMSystem(User):
    def __init__(self):
        self.users = []

    def add_user(self, user):
        self.users.append(user)

    def show_all(self):
        for user in self.users:
            print(user.view_data())
        


admin = Admin("Robert", "admin@crm.pl") 
client = Client("Anna", "anna@crm.pl")
cmr = CRMSystem()
cmr.add_user(admin)
cmr.add_user(client)

while True:
    try:

        info = input("Podaj czy jesteś adminem (A), czy Klientem (K)? Wyjście (Q) ").strip().lower()

        if info not in ["a","k","q"]:
            print("niepoprawna operacja, spróbuj jeszcze raz... ")
            continue
        if info == "q":
            print("Do widzenia")
            break
        elif info == "a":
            new_name = input("Podaj nową nazwę użytkownika: ")
            new_email = input("Podaj nowego emaila: ")
            admin.edit_profile(new_name, new_email)
            print(admin.view_data())
            cmr.show_all()

        elif info == "k":
            new_name = input("Podaj nową nazwę użytkownika: ")
            client.edit_profile(new_name)
            print(client.view_data())
   
    except ValueError as e:
        print(e)

# ============================================
# 🧾 KOMPLETNY OPIS LOGIKI PROGRAMU CRM
# ============================================

# 🔹 CEL PROGRAMU:
# Ten program tworzy prosty system CRM, który zarządza użytkownikami.
# Użytkownicy mogą być typu Admin lub Client. Każdy z nich ma inne uprawnienia
# do edytowania danych. Program działa w pętli, pozwalając użytkownikowi
# wybrać rolę i zaktualizować swoje dane.

# 🔹 STRUKTURA KLAS:
# 1. User — klasa bazowa, zawiera wspólne dane: name i email
# 2. Admin — dziedziczy po User, może edytować name i email
# 3. Client — dziedziczy po User, może edytować tylko name
# 4. CRMSystem — przechowuje listę użytkowników i zarządza nimi

# 🔹 DZIAŁANIE KLAS:
# class User:
# - Konstruktor __init__ zapisuje name i email
# - Metoda view_data() zwraca dane użytkownika w formacie tekstowym

# class Admin(User):
# - Dziedziczy name i email z User
# - Metoda edit_profile(new_name, new_email) pozwala zmienić oba pola
# - Nadpisuje view_data(), dodając komunikat "Panel Administratora"

# class Client(User):
# - Dziedziczy name i email z User
# - Metoda edit_profile(new_name) pozwala zmienić tylko name
# - Nadpisuje view_data(), pokazując tylko nazwę użytkownika

# class CRMSystem:
# - Konstruktor tworzy pustą listę users
# - add_user(user) dodaje obiekt typu User/Admin/Client do listy
# - show_all() wypisuje dane wszystkich użytkowników z listy
#   (wykorzystuje polimorfizm — każdy obiekt ma własną wersję view_data())

# 🔹 PRZEPŁYW DANYCH W PROGRAMIE:
# 1. Tworzymy obiekty admin i client z danymi startowymi
# 2. Tworzymy obiekt cmr typu CRMSystem
# 3. Dodajemy admina i klienta do systemu przez cmr.add_user()
# 4. Program wchodzi w pętlę while True — użytkownik wybiera rolę:
#    - "a" → admin: może zmienić nazwę i email
#    - "k" → klient: może zmienić tylko nazwę
#    - "q" → wyjście z programu
# 5. Po edycji danych wywoływana jest metoda view_data() dla danego użytkownika
# 6. Wywoływana jest cmr.show_all(), która wypisuje wszystkich użytkowników

# 🔹 POWIĄZANIA I ZALEŻNOŚCI:
# - Admin i Client są obiektami typu User → dziedziczą jego pola i metody
# - CRMSystem przechowuje listę obiektów User (w tym Admin i Client)
# - Metoda show_all() działa na zasadzie polimorfizmu — każdy obiekt
#   reaguje na view_data() zgodnie z własną klasą
# - Edycja danych zmienia stan obiektu — ponieważ CRMSystem przechowuje
#   referencje do tych obiektów, zmiany są widoczne globalnie

# 🔹 ZASADY OOP WYKORZYSTANE W PROGRAMIE:
# - Dziedziczenie: Admin i Client dziedziczą po User
# - Polimorfizm: każda klasa ma własną wersję metody view_data()
# - Enkapsulacja: dane użytkownika są modyfikowane tylko przez metody edit_profile()
# - Abstrakcja: CRMSystem ukrywa szczegóły zarządzania użytkownikami

# 🔹 CO MOŻNA ROZBUDOWAĆ:
# - Dodać logowanie z hasłem
# - Dodać filtrowanie użytkowników
# - Dodać zapis do pliku lub bazy danych
# - Dodać testy jednostkowe (np. unittest, pytest)


    

