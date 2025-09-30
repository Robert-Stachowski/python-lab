# 6. Klasa Employee
# Utwórz klasę Employee z polami: name, salary.
# Dodaj metodę get_info(), która zwraca string:
# "<name> zarabia <salary> zł"
# Stwórz 2 pracowników i wypisz informacje o nich.
# TODO
class Employee:
    def __init__(self,name,salary):
        self.name = name
        self.salary = salary

    def get_info(self):
        return f"{self.name} zarabia {self.salary} zł"
    
    def __str__(self):
        return self.get_info()
    

employers = [Employee("Michał", 5000), Employee("Edmund", 4800)]

for emp in employers:
    print(emp.get_info())
    #print(emp) - też zadziała, bo __str__ korzysta z get_info()
        

print("="*40)


# 7. Dziedziczenie - Konto bankowe
# Utwórz klasę BankAccount (owner, balance).
# Dodaj metody deposit(amount), withdraw(amount).
# Utwórz klasę SavingsAccount, która dziedziczy po BankAccount
# i dodaje pole interest_rate oraz metodę add_interest()
# (zwiększa saldo o odsetki).
# Przetestuj działanie w pętli.
# TODO

class BankAccount:
    def __init__(self,owner, balance):
        self.owner = owner
        self.__balance = balance
        
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            return self.__balance
        return "Błąd wpłata tylko powyżej zera"
    
    def withdraw(self, amount):
        if amount > self.__balance:
            return "Błąd, wypłata tylko do maksymalnej wartości salda"
        if amount < 0:
            return "Wypłaty tylko wartości większych niż zero"
        self.__balance -= amount
        return self.__balance
    
    def show_balance(self):
        return self.__balance
    
class SavingsAccount(BankAccount):
    def __init__(self, owner, balance, interest_rate=0.05):
        super().__init__(owner, balance)
        self.interest_rate = interest_rate

    def add_interest(self):
        interest = self.interest_rate * self.show_balance()
        self.deposit(interest)
        return self.show_balance()
    

person = BankAccount("Mirek", 1000)
saver = SavingsAccount("Mirek", 1000, 0.05)
person.deposit(200)
print(person.show_balance())
person.withdraw(300)
print(person.show_balance())

for i in range(3):
    print(f"\nSaldo przed odsetkami: {saver.show_balance()} zł")
    saver.add_interest()
    print(f"Saldo po odsetkach: {saver.show_balance()} zł\n")

print("="*40)


# 8. Polimorfizm - Instrumenty muzyczne
# Utwórz klasę Instrument z metodą play().
# Utwórz klasy Guitar i Piano, które nadpisują play()
# odpowiednio: "Brzdękam na gitarze", "Gram na pianinie".
# W pętli po liście instrumentów wywołaj play().
# TODO

class Instrument:
    def play(self):
        return "Gram sobie"
    
class Guitar(Instrument):
    def play(self):
        return "Brzdękam na gitarze"
    
    def __str__(self):
        return self.play()
    
class Piano(Instrument):
    def play(self):
        return "Gram na pianinie"

    def __str__(self):
        return self.play()
    

instruments = [Guitar(),Piano(),Guitar()]

for i in instruments:
    print(i)

print("="*40)


# 9. Kompozycja - Koszyk w sklepie
# Utwórz klasę Product (name, price).
# Utwórz klasę Cart, która ma listę produktów.
# Dodaj metody:
# - add_product(product)
# - total_price() -> zwraca sumę cen produktów
# Stwórz koszyk, dodaj kilka produktów i oblicz łączną cenę.
# TODO

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Cart:
    def __init__(self):
        self.product_list = []

    def add_product(self, product):
        self.product_list.append(product)

    def total_price(self):
        return sum(product.price for product in self.product_list)

crt = Cart()

while True:
    try:
        input_data = input("Dodaj produkt oraz cenę, rozdziel przecinkiem (lub wpisz 'q' aby zakończyć): ").strip()

        if input_data.lower() == "q":
            print(f"\nŁączna wartość koszyka: {crt.total_price()} zł")
            break

        parts = [p.strip() for p in input_data.split(",") if p.strip()]
        if len(parts) != 2:
            print("Podaj dokładnie dwa elementy: nazwę i cenę.")
            continue

        name = parts[0]
        price = float(parts[1])
        product = Product(name, price)
        crt.add_product(product)

    except ValueError as e:
        print(f"Błąd: {e}")
        continue
        
print("="*40)


# 10. Abstrakcja + super() - Zwierzęta
# Utwórz abstrakcyjną klasę Animal z metodą abstract speak().
# Dodaj konstruktor przyjmujący name i zapisujący go do self.
# Utwórz klasy Dog i Cat, które dziedziczą po Animal i
# implementują speak().
# W konstruktorach użyj super().__init__(name).
# W pętli wypisz "<name>: <speak()>"
# TODO

from abc import ABC,abstractmethod

class Animal(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "hau hau"
    
class Cat(Animal):
    def speak(self):
        return "Miau miau"
    
animals = [Dog("Mordka"),Cat("Bonifacy"),Dog("Nero")]

for a in animals:
    print(f"{a.name}: {a.speak()}")

print("="*40)

# Zadanie:
# Utwórz klasę Vehicle z konstruktorem __init__(self, brand)
# Utwórz klasę Car, która dziedziczy po Vehicle i dodaje model
# W konstruktorze Car użyj super().__init__(brand)
# Dodaj metodę info() wypisującą markę i model
# Cel:
# Zrozumienie, jak super() pozwala odziedziczyć dane i dodać nowe
 
class Vehicle:
    def __init__(self,brand):
        self.brand = brand
    
class Car(Vehicle):
    def __init__(self, brand,model):
        super().__init__(brand)
        self.model = model

    def info(self):
        return f"{self.brand} {self.model}"

cars = [Car("toyot","corolla"),Car("skoda","octavia")]
for car in cars:
    print(car.info())

# Zadanie:
# Utwórz klasę Person z konstruktorem __init__(self, name)
# Utwórz klasę Student, która dziedziczy po Person, ale nie dodaje nowych pól
# Zdefiniuj konstruktor w Student, który wywołuje super().__init__(name)
# Dodaj metodę introduce() wypisującą imię
# Cel:
# Zrozumienie, że nawet bez nowych pól warto świadomie użyć super()

class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name):
        super().__init__(name)

    def introduce(self):  
        return self.name
    
student = Student("michał")
print(student.introduce())

# Zadanie:
# Utwórz klasę abstrakcyjną Shape z konstruktorem __init__(self, name) i metodą abstrakcyjną area()
# Utwórz klasę Square, która dziedziczy po Shape, dodaje side, używa super().__init__(name)
# Zaimplementuj area() jako side * side
# Wypisz name i area() w pętli po liście figur

# 🔧 Co to ćwiczenie Ci da?
# - Połączysz dziedziczenie, abstrakcję, super() i logikę
# - Zobaczysz, jak super() pozwala odziedziczyć nazwę figury, a area() daje różne wyniki zależnie od klasy
# - Przygotujesz się na bardziej złożone struktury, jak np. Form, Model, View w web devie

from abc import ABC, abstractmethod

class Shape(ABC):
    def __init__(self,name):
        self.name = name

    @abstractmethod
    def area(self):
        pass

class Square(Shape):
    def __init__(self, name, side):
        super().__init__(name)
        self.side = side

    def area(self):
        return self.side*self.side
    
shape_list = [Square("kwadrat",3),Square("trójkąt",2),Square("masakra",4),Square("tybetańska",5)]

for s in shape_list:
    print(s.name, s.area())

# Zadanie:
# Utwórz klasę Base, która ma konstruktor __init__(self, value) i zapisuje self.value
# Utwórz klasę Child, która dziedziczy po Base, ale nie używa super()
# Spróbuj stworzyć obiekt Child("abc") i wypisać self.value

class Base:
    def __init__(self,value):
        self.value = value

class Child(Base):
    def __init__(self, value):
        super().__init__(value)        

    def __str__(self):
        return f"Child with value: {self.value}"


x = Child("abc")
print(x)


# Zadanie:
# - Utwórz klasę Employee z konstruktorem __init__(self, name, salary)
# - Dodaj metodę info(), która zwraca imię i pensję
# - Utwórz klasę Manager, która dziedziczy po Employee i dodaje team_size
# - W konstruktorze Manager użyj super().__init__(name, salary)
# - Nadpisz metodę info(), żeby zwracała imię, pensję i wielkość zespołu

# 🔧 Cel ćwiczenia:
# - Pokazać, jak super() pozwala odziedziczyć dane i logikę
# - Rozszerzyć klasę o nowe pole (team_size)
# - Nadpisać metodę info() i użyć super().info() w środku, jeśli chcesz
  
class Employee:
    def __init__(self,name, salary):
        self.name = name
        self.salary = salary

    def info(self):
        return f"Imie: {self.name}, Wynagrodzenie: {self.salary} zł"
    
class Manger(Employee):
    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)
        self.team_size = team_size

    def info(self):
        return super().info() + f", Zespół: {self.team_size}"
    

manager = Manger("Robert",13000,6)
print(manager.info())
        




