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
print("="*40)


# 9. Kompozycja - Koszyk w sklepie
# Utwórz klasę Product (name, price).
# Utwórz klasę Cart, która ma listę produktów.
# Dodaj metody:
# - add_product(product)
# - total_price() -> zwraca sumę cen produktów
# Stwórz koszyk, dodaj kilka produktów i oblicz łączną cenę.
# TODO
print("="*40)


# 10. Abstrakcja + super() - Zwierzęta
# Utwórz abstrakcyjną klasę Animal z metodą abstract speak().
# Dodaj konstruktor przyjmujący name i zapisujący go do self.
# Utwórz klasy Dog i Cat, które dziedziczą po Animal i
# implementują speak().
# W konstruktorach użyj super().__init__(name).
# W pętli wypisz "<name>: <speak()>"
# TODO
print("="*40)
