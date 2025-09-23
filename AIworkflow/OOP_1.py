# ===============================================
# 1. Klasa prostokąta
# Zbuduj klasę Rectangle z atrybutami: width, height.
# Dodaj metodę area(), która zwróci pole prostokąta.
# TODO

class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):        
        return self.width * self.height


rect1 = Rectangle(7,5)
print(rect1.area())

# ===============================================


# ===============================================
# 2. Klasa samochodu 
# Utwórz klasę Car z atrybutami: brand, model, year.
# Dodaj metodę start(), która wypisze np. "Samochód Tesla Model S rusza!".
# TODO
class Car:
    def __init__(self,brand,model,year):
        self.brand = brand
        self.model = model
        self.year = year

    def start(self):
        return f"Samochód {self.brand} {self.model} rusza!"
    
tesla = Car("tesla", "model S",2022)
print(tesla.start())

# ===============================================




# ===============================================
# 3. Klasa bankowego konta
# Utwórz klasę BankAccount z atrybutem balance.
# Dodaj metody: deposit(amount), withdraw(amount), show_balance().
# TODO

class BankAccount:
    def __init__(self, balance):
        self.__balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            return True
        return False
    
    def withdraw(self, amount):
        if amount > 0 and amount <= self.__balance:
            self.__balance -= amount
            return True
        return False
    
    def show_balance(self):
        return self.__balance
    
bank = BankAccount(1000)
bank.deposit(200)
bank.withdraw(500)
print(bank.show_balance())

# ===============================================


# ===============================================
# 4. Dziedziczenie – Zwierzęta
# Utwórz klasę Animal z metodą sound() → "Some generic sound".
# Utwórz klasy Dog i Cat dziedziczące po Animal,
# które nadpisują metodę sound() odpowiednio: "Woof!" i "Meow!".
# TODO

class Animal:
    def sound(self):
        return "Some generic sound"
    
class Dog(Animal):
    def sound(self):
        return "Woof"
    
class Cat(Animal):
    def sound(self):
        return "Meow"
    
animal = Animal()
dog = Dog()
cat = Cat()
        
print(animal.sound(), dog.sound(), cat.sound())
 
# ===============================================


# ===============================================
# 5. Polimorfizm – Lista pojazdów
# Utwórz klasę Vehicle z metodą move() (np. "Pojazd się porusza").
# Utwórz klasy Car i Plane, które nadpisują metodę move()
# (np. "Samochód jedzie" i "Samolot leci").
# W main utwórz listę z różnymi pojazdami i przeiteruj pętlą,
# wywołując move() na każdym obiekcie.
# TODO

class Vehicle:
    def move(self):
        return "Pojazd się porusza"
    
class Car(Vehicle):
    def move(self):
        return "Samochód się porusza"
    
class Plane(Vehicle):
    def move(self):
        return "Samolot leci"
    
vehicles = [Vehicle(),Car(),Plane()]

for v in vehicles:
    print(v.move())

# ===============================================
# ===============================================
# 6. __str__ – ładne drukowanie obiektów
# Utwórz klasę Book z atrybutami: title, author, year.
# Dodaj metodę __str__ tak, aby print(book) wypisywał np.:
# "Tytuł: Hobbit, Autor: Tolkien (1937)".
# TODO

class Book:
    def __init__(self,title,author,year):
        self.title = title
        self.author = author
        self.year = year

    def __str__(self):
        return f"Tytuł: {self.title}, Autor: {self.author} ({self.year})"

book = Book("Hobbit","Tolkien",1937)
print(book)


# ===============================================


# ===============================================
# 7. Porównywanie obiektów (__eq__)
# Utwórz klasę Student z atrybutami: name, student_id.
# Dodaj metodę __eq__, aby dwóch studentów było uznanych
# za równych, jeśli mają takie samo student_id.
# TODO

class Student:
    def __init__(self,name,student_id):
        self.name = name
        self.student_id = student_id

    def __eq__(self, other):
        return self.student_id == other.student_id
        


student1 = Student("Marek", 100)
student2 = Student("Roman", 100)

if student1 == student2:
    print("ok")
else:
    print("not ok")
# ===============================================


# ===============================================
# 8. Abstrakcyjna klasa Shape
# Użyj modułu abc (abstract base class).
# Utwórz klasę Shape z abstrakcyjną metodą area().
# Utwórz klasy Circle i Square, które implementują area().
# W main utwórz listę figur i policz ich pola.
# TODO
from abc import ABC, abstractmethod
import math


class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius        

    def area(self):             
        return math.pi * (self.radius**2)

class Square(Shape):
    def __init__(self,side):
        self.side = side
        
    def area(self):
        return self.side**2
    
shape_list = [Circle(5),Square(7)]
for s in shape_list:
    print(s.area())

# ===============================================


# ===============================================
# 9. Dziedziczenie wielopoziomowe
# Utwórz klasę Person (name).
# Utwórz klasę Employee (dziedziczy po Person, ma salary).
# Utwórz klasę Manager (dziedziczy po Employee, ma team_size).
# Dodaj metody show_info() w każdej klasie, aby rozszerzały dane.
# TODO

class Person:
    def __init__(self, name):
        self.name = name

    def show_info(self):
        return f"Imię: {self.name}"

class Employee(Person):
    def __init__(self,name, salary):
        super().__init__(name)
        self.salary = salary

    def show_info(self):
        base = super().show_info()
        return f"{base}, Pensja: {self.salary}"

class Manger(Employee):
    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)
        self.team_size = team_size

    def show_info(self):
        base = super().show_info()
        return f"{base}, Zespół: {self.team_size}"
    
obj_list = [Person("Wacek"), Employee("Mirek",7000), Manger("Michał",7000,12)]
for o in obj_list:
    print(o.show_info())




# ===============================================


# ===============================================
# 10. Polimorfizm + praktyczne użycie
# Utwórz klasę Notification z metodą send().
# Utwórz klasy EmailNotification i SMSNotification,
# które nadpisują send() w odpowiedni sposób.
# W main utwórz listę powiadomień i przeiteruj je w pętli.
# TODO

class Notification:
    def send(self):
        return "Powiadomienie ogólne"

class EmailNotification(Notification):
    def send(self):
        return "Powiadomienie Email"
        
class SMSNotification(Notification):
    def send(self):
        return "Powiadomienie SMS"

notif_list = [Notification(),EmailNotification(),SMSNotification()]

for n in notif_list:
    print(n.send())

# ===============================================
