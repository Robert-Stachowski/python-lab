# ===============================================
# 11. Dziedziczenie + __str__
# Utwórz klasę Vehicle (brand, year) z czytelnym __str__.
# Utwórz klasy Car i Bike dziedziczące po Vehicle:
# - Car dodaje doors
# - Bike dodaje rim_size
# Każda klasa nadpisuje __str__, korzystając z super().__str__().

class Vehicle:
    def __init__(self, brand, year):
        # Klasa bazowa przechowuje wspólne pola: marka i rok.
        self.brand = brand
        self.year = year

    def __str__(self):
        # Reprezentacja tekstowa dla Vehicle:
        return f"{self.brand} z {self.year}"

class Bike(Vehicle):
    def __init__(self, brand, year, rim_size):
        # Wołamy konstruktor klasy bazowej, by ustawić brand/year.
        super().__init__(brand, year)
        # Pole specyficzne dla Bike: rozmiar obręczy (w calach).
        self.rim_size = rim_size

    def __str__(self):
        # Bazowy fragment (marka + rok) bierzemy z Vehicle.__str__().
        base = super().__str__()
        # Rozszerzamy opis o to, co specyficzne dla Bike.
        return f"{base} — felgi {self.rim_size}\""

class Car(Vehicle):
    def __init__(self, brand, year, doors):
        # Ponownie inicjalizujemy część wspólną (brand/year).
        super().__init__(brand, year)
        # Pole specyficzne dla Car: liczba drzwi.
        self.doors = doors

    def __str__(self):
        # Znowu budujemy na bazowej reprezentacji i dokładamy szczegóły.
        base = super().__str__()
        return f"{base} — drzwi: {self.doors}"

# Przykładowe obiekty i wypisywanie:
vehicles = [
    Vehicle("Generic", 1999),
    Bike("Kross", 2021, 29),
    Car("Skoda Octavia", 2018, 5),
]

for v in vehicles:
    # Dzięki __str__ każdy obiekt wypisze się w czytelnej, klasowej formie.
    print(v)

# ===============================================



# ===============================================
# 12. Książki w bibliotece
# Utwórz klasę Book (title, author).
# Utwórz klasę Library, która przechowuje listę książek.
# Dodaj metody: add_book(), show_books().
# TODO

class Book:
    def __init__(self,title,author):
        self.title = title
        self.author = author

    def __str__(self):
        return f"Tytuł: {self.title}, Autor: {self.author}"

class Library:
    def __init__(self):
        self.lib_list = []

    def add_book(self, new_book):
        self.lib_list.append(new_book)

    def show_books(self):
        if not self.lib_list:
            print("Brak książek")
        else:
            print("\n--- Książki w bibliotece: ---")
            for book in self.lib_list:
                print(book)
            print("-------------------------\n")

library = Library()

while True:
    try:
        operation = input("Podaj nazwę książki i autora, oddziel przecinkiem, lub q jako wyjście: ")
        parts = [p.strip() for p in operation.split(",") if p.strip()]

        if operation== "q":
            library.show_books()
            break

        if len(parts) != 2:
            print("Proszę podać Tytuł i Autora, oddzielone przecinkami!")
            continue

        title = parts[0]
        author = parts[1]
        new_book = Book(title,author)
        

        library.add_book(new_book)
        library.show_books()
        break
    
    except ValueError as e:
        print(f"Błąd: {e}")
        continue
# ===============================================


# ===============================================
# 13. Konto premium
# Utwórz klasę BankAccount (balance, deposit, withdraw).
# Utwórz klasę PremiumAccount, która dziedziczy po BankAccount
# i dodaje metodę give_bonus(), np. +5% salda.
# TODO

class BankAccount:
    def __init__(self, balance):
        self.__balance = balance

    def deposit(self, amount):
        self.__balance += amount


    def withdraw(self, amount):
        self.__balance -= amount

    def show_balance(self):
        return self.__balance
    
    def update_balance(self, new_value):
        self.__balance = new_value

class PremiumAccount(BankAccount):
    def __init__(self, balance):
        super().__init__(balance)

    def give_bonus(self):        
        new_balance = self.show_balance() * 1.05
        self.update_balance(new_balance)
        





# ===============================================


# ===============================================
# 14. Abstrakcyjna klasa Worker
# Utwórz klasę abstrakcyjną Worker z metodą work().
# Utwórz klasy Programmer i Teacher, które implementują work()
# (np. "Pisze kod", "Prowadzi lekcję").
# W pętli przeiteruj listę pracowników i wywołaj work().
# TODO

from abc import ABC, abstractmethod

class Worker(ABC):
    @abstractmethod
    def work(self):
        pass

class Programmer(Worker):
    def __init__(self):
        pass

    def work(self):
        return "Pisze kod"
    
class Teacher(Worker):
    def __init__(self):
        pass

    def work(self):
        return "Prowadzi lekcje"



worker_list = [Programmer(), Teacher()]

for w in worker_list:
    print(w.work())


# ===============================================


# ===============================================
# 15. Polimorfizm – sklep internetowy
# Utwórz klasę Product z metodą get_price().
# Utwórz klasy BookProduct i FoodProduct, które nadpisują get_price()
# (np. książki mają VAT 5%, jedzenie 8%).
# W main oblicz łączną cenę zakupów z listy produktów.
# TODO

class Product:
    def __init__(self, product, price):
        self.product = product
        self.price = price

    def get_price(self):
        return self.price 
         

class BookProduct(Product):
    def __init__(self, product, price):
        super().__init__(product, price)
        

    def get_price(self):
        book_price = self.price * 1.05
        return book_price
    
class FoodProduct(Product):
    def __init__(self, product, price):
        super().__init__(product, price)
        

    def get_price(self):
        food_price = self.price *1.08
        return food_price
    

product_list = [BookProduct("Książka o inwestowaniu", 100), FoodProduct("Ryba w puszce", 13.4)]

for p in product_list:
    print(f"{p.product} - {p.get_price():.2f} zł")



# ===============================================
# 1. Klasa Student
# Utwórz klasę Student z polami: name, age, grade.
# Dodaj metodę get_info(), która zwróci string:
# "Imię: <name>, Wiek: <age>, Ocena: <grade>"
# Stwórz 2 obiekty i wypisz ich informacje.
# TODO

class Student:
    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade

    def __str__(self):
        return f"Imię: {self.name}, Wiek: {self.age}, Ocena: {self.grade}"


students_one = Student("Jacek", 24, "4+")
students_two = Student("Michał", 33, "3+")

print(students_one)
print(students_two)

# LUB:

# students_one = ("Jacek", 24, "4+")    - krotka
# students_two = ("Michał", 33, "3+")  - krotka
# print(Student(*students_one)) - * rozpakowanie krotki na pozycje
# print(Student(*students_two)) - * rozpakowanie krotki na pozycje


print("="*40)


# 2. Dziedziczenie - Zwierzęta
# Utwórz klasę Animal z polem species i metodą speak().
# Utwórz klasy Dog i Cat, które dziedziczą po Animal
# i nadpisują metodę speak():
# - Dog: "Woof!"
# - Cat: "Meow!"
# W pętli wywołaj speak() dla listy zwierząt.
# TODO

class Animal:
    def __init__(self, species):
        self.species = species

    def speak(self):
        return "Zwierzę wydaje dźwięk"

class Dog(Animal):
    def speak(self):
        return "Dog: Woof!"
    
class Cat(Animal):
    def speak(self):
        return "Cat Meow!"


animals = [Dog("szczeka"),Cat("maiuczy"),Dog("szczeka")]

for a in animals:
    print(a.speak())



print("="*40)


# 3. Polimorfizm - Figura geometryczna
# Utwórz klasę Shape z metodą area().
# Utwórz klasy Circle (pole: radius) i Rectangle (fields: width, height),
# które nadpisują area() i liczą pole powierzchni.
# W pętli oblicz pola figur z listy [Circle, Rectangle].
# TODO
import math

class Shape:
    def __init__(self):
        pass


    def area(self):
        return "Pole powierzchni"
    
class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi*(self.radius**2)

class Rectangle(Shape):
    def __init__(self, width, height):
        self.height = height
        self.width = width

    def area(self):
        return self.width*self.height

shapes = [Circle(5), Rectangle(4,4)]

for s in shapes:
    print(f"{s.area():.2f}")





print("="*40)


# 4. Książka i Biblioteka
# Utwórz klasę Book (title, author).
# Dodaj klasę Library, która przechowuje listę książek (books).
# Library ma metody:
# - add_book(book)
# - show_books() -> wypisuje wszystkie tytuły i autorów
# Stwórz obiekt biblioteki, dodaj kilka książek i wyświetl listę.
# TODO

class Book:
    def __init__(self,title,author):
        self.title = title
        self.author = author

    def __str__(self):
        return f"Tytuł: {self.title}, Autor: {self.author}"


class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def show_books(self):
        if not self.books:
             print("Pusta lista książek")
        for book in self.books:
            print(book)
    

list_books = [("hjfbjfh","hbfjhfbjhf"),("jjjjjjsssssssss","nddddbdbd"),("aaaaaaaaa","eeeeeee")]
library = Library()

for title,author in list_books:
    book = Book(title,author)
    library.add_book(book)

library.show_books()
    



print("="*40)


# 5. Abstrakcja - Pojazdy
# Utwórz klasę abstrakcyjną Vehicle z metodą abstract move().
# Utwórz klasy Car i Plane, które implementują move():
# - Car: "Jadę po drodze"
# - Plane: "Lecę w powietrzu"
# W pętli wywołaj move() dla listy pojazdów.
# TODO

from abc import ABC,abstractmethod

class Vehicle(ABC):
    @abstractmethod
    def move(self):
        pass


class Car(Vehicle):
    def __init__(self):
        pass

    def move(self):
        return "Jadę po drodze"
    
class Plane(Vehicle):
    def __init__(self):
        pass

    def move(self):
        return "Lecę w powietrzu"
    

vehicles = [Car(),Plane(),Plane(),Car()]

for v in vehicles:
    print(v.move())

print("="*40)
