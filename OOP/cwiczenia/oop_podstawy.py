# ===============================================
# 1. Klasa prostokąta
# Zbuduj klasę Rectangle z atrybutami: width, height.
# Dodaj metodę area(), która zwróci pole prostokąta.

class Rectangle:
    def __init__(self, width, height):
        # Konstruktor: zapisuje szerokość i wysokość w atrybutach instancji.
        # self.width i self.height będą dostępne w innych metodach obiektu.
        self.width = width
        self.height = height

    def area(self):
        # Metoda instancyjna licząca pole prostokąta.
        # Odwołujemy się do atrybutów obiektu przez self.
        return self.width * self.height


# Tworzymy obiekt Rectangle o szerokości 7 i wysokości 5.
rect1 = Rectangle(7, 5)

# Wywołujemy metodę area() i wypisujemy wynik.
print(rect1.area())

# ===============================================


# ===============================================
# 2. Klasa samochodu 
# Utwórz klasę Car z atrybutami: brand, model, year.
# Dodaj metodę start(), która wypisze np. "Samochód Tesla Model S rusza!".

class Car:
    def __init__(self, brand, model, year):
        # Konstruktor: zapisuje markę, model i rok produkcji.
        self.brand = brand
        self.model = model
        self.year = year

    def start(self):
        # Metoda zwraca komunikat, nie drukuje go bezpośrednio
        # (to dobra praktyka: logika zwraca dane, a "print" robimy na zewnątrz).
        return f"Samochód {self.brand} {self.model} rusza!"
    

# Tworzymy obiekt Car: marka "tesla", model "model S", rok 2022.
tesla = Car("tesla", "model S", 2022)

# Drukujemy to, co zwraca start().
print(tesla.start())

# ===============================================





# ===============================================
# 3. Klasa bankowego konta
# Utwórz klasę BankAccount z atrybutem balance.
# Dodaj metody: deposit(amount), withdraw(amount), show_balance().

class BankAccount:
    def __init__(self, balance):
        # __balance: "name mangling" (podwójny podkreślnik) utrudnia bezpośredni dostęp z zewnątrz.
        # Konwencja OOP: chronimy stan konta przed przypadkową modyfikacją.
        self.__balance = balance

    def deposit(self, amount):
        # Wpłata: dodajemy kwotę do salda tylko, jeśli jest dodatnia.
        if amount > 0:
            self.__balance += amount
            return True  # zwracamy True, by z zewnątrz łatwo sprawdzić sukces operacji
        return False     # kwota nieprawidłowa -> brak zmiany stanu

    def withdraw(self, amount):
        # Wypłata: możliwa, gdy amount > 0 oraz nie przekracza salda.
        if amount > 0 and amount <= self.__balance:
            self.__balance -= amount
            return True   # wypłata udana
        return False      # odrzucona: za duża kwota lub <= 0

    def show_balance(self):
        # Zwracamy saldo (nie drukujemy — to caller decyduje, co zrobić z wynikiem).
        return self.__balance
    

# Tworzymy konto z początkowym saldem 1000.
bank = BankAccount(1000)

# Wpłacamy 200 -> saldo: 1200 (jeśli True).
bank.deposit(200)

# Wypłacamy 500 -> saldo: 700 (jeśli True).
bank.withdraw(500)

# Drukujemy aktualne saldo.
print(bank.show_balance())

# ===============================================


# ===============================================
# 4. Dziedziczenie – Zwierzęta
# Utwórz klasę Animal z metodą sound() → "Some generic sound".
# Utwórz klasy Dog i Cat dziedziczące po Animal,
# które nadpisują metodę sound() odpowiednio: "Woof!" i "Meow!".

class Animal:
    def sound(self):
        # Domyślna metoda sound() w klasie bazowej.
        # Każde zwierzę umie wydawać jakiś dźwięk.
        return "Some generic sound"
    
class Dog(Animal):
    def sound(self):
        # Nadpisujemy metodę sound() z klasy Animal.
        # Polimorfizm: obiekt Dog zachowuje się inaczej niż Animal.
        return "Woof"
    
class Cat(Animal):
    def sound(self):
        # Nadpisujemy metodę sound() – wersja dla kota.
        return "Meow"
    

# Tworzymy obiekty każdej klasy.
animal = Animal()
dog = Dog()
cat = Cat()
        
# Wywołujemy sound() na każdym z obiektów.
# Każdy obiekt zwraca inny rezultat zgodnie z własną klasą.
print(animal.sound(), dog.sound(), cat.sound())

# ===============================================



# ===============================================
# 5. Polimorfizm – Lista pojazdów
# Utwórz klasę Vehicle z metodą move() (np. "Pojazd się porusza").
# Utwórz klasy Car i Plane, które nadpisują metodę move()
# (np. "Samochód jedzie" i "Samolot leci").
# W main utwórz listę z różnymi pojazdami i przeiteruj pętlą,
# wywołując move() na każdym obiekcie.

class Vehicle:
    def move(self):
        # Metoda domyślna: ogólny ruch pojazdu.
        return "Pojazd się porusza"
    
class Car(Vehicle):
    def move(self):
        # Nadpisanie metody move() – konkretna wersja dla samochodu.
        return "Samochód się porusza"
    
class Plane(Vehicle):
    def move(self):
        # Nadpisanie metody move() – konkretna wersja dla samolotu.
        return "Samolot leci"
    

# Tworzymy listę z obiektami różnych klas.
# Mimo że wszystkie są typu Vehicle (albo jego podklas),
# każdy obiekt zareaguje inaczej na wywołanie move().
vehicles = [Vehicle(), Car(), Plane()]

# Polimorfizm: ta sama metoda move() działa różnie w zależności od obiektu.
for v in vehicles:
    print(v.move())

# ===============================================



# ===============================================
# 6. __str__ – ładne drukowanie obiektów
# Utwórz klasę Book z atrybutami: title, author, year.
# Dodaj metodę __str__ tak, aby print(book) wypisywał np.:
# "Tytuł: Hobbit, Autor: Tolkien (1937)".

class Book:
    def __init__(self, title, author, year):
        # Konstruktor przypisuje atrybuty do obiektu.
        self.title = title
        self.author = author
        self.year = year

    def __str__(self):
        # __str__ to „magiczna metoda” – Python używa jej przy print().
        # Dzięki temu obiekt Book sam wie, jak ma wyglądać w tekście.
        return f"Tytuł: {self.title}, Autor: {self.author} ({self.year})"

# Tworzymy obiekt Book.
book = Book("Hobbit", "Tolkien", 1937)

# Drukujemy obiekt – Python wywoła __str__ i pokaże ładny opis.
print(book)

# ===============================================



# ===============================================
# 7. Porównywanie obiektów (__eq__)
# Cel: Dwóch studentów jest "równych", jeśli mają ten sam student_id.

class Student:
    def __init__(self, name, student_id):
        # Konstruktor: zapisujemy imię i unikalny identyfikator studenta.
        self.name = name
        self.student_id = student_id

    def __eq__(self, other):
        # __eq__ to metoda odpowiedzialna za operator ==
        # Porównujemy dwa obiekty Student po polu student_id.
        # Uwaga: w realnym kodzie warto dodać sprawdzenie typu (isinstance).
        return self.student_id == other.student_id


# Tworzymy dwóch studentów: ci sami ID -> powinni być "równi".
student1 = Student("Marek", 100)
student2 = Student("Roman", 100)

# Operator == wywoła Student.__eq__.
if student1 == student2:
    print("ok")       # Spodziewany wynik: "ok"
else:
    print("not ok")
# ===============================================



# ===============================================
# 8. Abstrakcyjna klasa Shape
# Używamy modułu abc do zdefiniowania klasy bazowej z metodą abstrakcyjną area().
# Klasy pochodne (Circle, Square) muszą tę metodę zaimplementować.

from abc import ABC, abstractmethod
import math

class Shape(ABC):
    @abstractmethod
    def area(self):
        # Metoda abstrakcyjna: brak implementacji.
        # Każda klasa dziedzicząca musi dostarczyć własną wersję area().
        pass

class Circle(Shape):
    def __init__(self, radius):
        # Konstruktor: promień koła.
        self.radius = radius

    def area(self):
        # Implementacja wzoru na pole koła: π * r^2
        return math.pi * (self.radius ** 2)

class Square(Shape):
    def __init__(self, side):
        # Konstruktor: długość boku kwadratu.
        self.side = side

    def area(self):
        # Implementacja wzoru na pole kwadratu: a^2
        return self.side ** 2

# Tworzymy listę różnych figur (polimorfizm na poziomie interfejsu area()).
shape_list = [Circle(5), Square(7)]

# Każdy obiekt ma metodę area(), ale implementacje są różne.
for s in shape_list:
    print(s.area())
# ===============================================



# ===============================================
# 9. Dziedziczenie wielopoziomowe
# Person (name) -> Employee (salary) -> Manager (team_size)
# Każda klasa rozbudowuje show_info() o własne pola.
# Uwaga: w oryginalnym pliku była literówka "Manger"; tu w komentarzach nazywamy "Manager".

class Person:
    def __init__(self, name):
        # Klasa bazowa: ma tylko imię.
        self.name = name

    def show_info(self):
        # Zwraca podstawowe informacje o osobie.
        return f"Imię: {self.name}"

class Employee(Person):
    def __init__(self, name, salary):
        # Wywołujemy konstruktor Person, by zainicjalizować name.
        super().__init__(name)
        # Dodajemy własne pole: pensja.
        self.salary = salary

    def show_info(self):
        # Rozszerzamy show_info() z klasy bazowej o pensję.
        base = super().show_info()
        return f"{base}, Pensja: {self.salary}"

class Manger(Employee):
    # Zachowujemy oryginalną nazwę klasy z Twojego pliku (Manger),
    # ale logicznie powinna nazywać się "Manager".
    def __init__(self, name, salary, team_size):
        # Inicjalizujemy część Employee (a przez to Person).
        super().__init__(name, salary)
        # Dodajemy rozmiar zespołu zarządzanego przez menedżera.
        self.team_size = team_size

    def show_info(self):
        # Ponownie rozszerzamy show_info() o rozmiar zespołu.
        base = super().show_info()
        return f"{base}, Zespół: {self.team_size}"

# Tworzymy po jednym obiekcie każdej klasy i sprawdzamy kaskadowe show_info().
obj_list = [Person("Wacek"), Employee("Mirek", 7000), Manger("Michał", 7000, 12)]
for o in obj_list:
    print(o.show_info())
# ===============================================



# ===============================================
# 10. Polimorfizm + praktyczne użycie
# Utwórz klasę Notification z metodą send().
# Utwórz klasy EmailNotification i SMSNotification,
# które nadpisują send() w odpowiedni sposób.
# W main utwórz listę powiadomień i przeiteruj je w pętli.

class Notification:
    def send(self):
        # Metoda bazowa: ogólny komunikat dla "jakiegoś" powiadomienia.
        return "Powiadomienie ogólne"

class EmailNotification(Notification):
    def send(self):
        # Nadpisanie (override) dla e-maila: specyficzna implementacja.
        return "Powiadomienie Email"
        
class SMSNotification(Notification):
    def send(self):
        # Nadpisanie (override) dla SMS: specyficzna implementacja.
        return "Powiadomienie SMS"

# Lista obiektów różnych podklas ma ten sam interfejs: .send().
# Polimorfizm: wywołanie .send() na każdym elemencie robi "coś swojego".
notif_list = [Notification(), EmailNotification(), SMSNotification()]

for n in notif_list:
    # Dla każdego elementu wywołujemy metodę o tej samej nazwie.
    # Wynik zależy od *konkretnej* klasy obiektu (dynamiczny dispatch).
    print(n.send())

# ===============================================

