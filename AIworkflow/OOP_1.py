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






# ===============================================


# ===============================================
# 3. Klasa bankowego konta
# Utwórz klasę BankAccount z atrybutem balance.
# Dodaj metody: deposit(amount), withdraw(amount), show_balance().
# TODO
# ===============================================


# ===============================================
# 4. Dziedziczenie – Zwierzęta
# Utwórz klasę Animal z metodą sound() → "Some generic sound".
# Utwórz klasy Dog i Cat dziedziczące po Animal,
# które nadpisują metodę sound() odpowiednio: "Woof!" i "Meow!".
# TODO
# ===============================================


# ===============================================
# 5. Polimorfizm – Lista pojazdów
# Utwórz klasę Vehicle z metodą move() (np. "Pojazd się porusza").
# Utwórz klasy Car i Plane, które nadpisują metodę move()
# (np. "Samochód jedzie" i "Samolot leci").
# W main utwórz listę z różnymi pojazdami i przeiteruj pętlą,
# wywołując move() na każdym obiekcie.
# TODO
# ===============================================
