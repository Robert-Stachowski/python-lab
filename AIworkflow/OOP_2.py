# ===============================================
# 11. Dziedziczenie + __str__
# Utwórz klasę Vehicle (brand, year).
# Utwórz klasy Car i Bike, które dziedziczą po Vehicle
# i dodają swoje pola (np. doors, type).
# Dodaj __str__ tak, aby print() wypisywał pełne dane.
# TODO

class Vehicle:
    def __init__(self,brand,year):
        self.brand = brand
        self.year = year

    def __str__(self):
        return f"{self.brand} z {self.year}"

class Bike(Vehicle):
    def __init__(self, brand, year, rim_size):
        super().__init__(brand, year)
        self.rim_size = rim_size

    def __str__(self):
        base = super().__str__()
        return f"{base} ma felgi {self.rim_size} cali"

class Car(Vehicle):
    def __init__(self, brand, year, doors):
        super().__init__(brand, year)
        self.doors = doors

    def __str__(self):
        base = super().__str__()
        return f"{base} ma {self.doors} drzwi!"


vehicles = [Vehicle("pojazd", 2007), Bike("Cross", 2024, 29), Car("Tesla",2025, 4)]
for v in vehicles:
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
# ===============================================


# ===============================================
# 14. Abstrakcyjna klasa Worker
# Utwórz klasę abstrakcyjną Worker z metodą work().
# Utwórz klasy Programmer i Teacher, które implementują work()
# (np. "Pisze kod", "Prowadzi lekcję").
# W pętli przeiteruj listę pracowników i wywołaj work().
# TODO
# ===============================================


# ===============================================
# 15. Polimorfizm – sklep internetowy
# Utwórz klasę Product z metodą get_price().
# Utwórz klasy BookProduct i FoodProduct, które nadpisują get_price()
# (np. książki mają VAT 5%, jedzenie 8%).
# W main oblicz łączną cenę zakupów z listy produktów.
# TODO
# ===============================================
