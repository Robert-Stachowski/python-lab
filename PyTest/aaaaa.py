class Car:
    def __init__(self,brand,year):
        self.brand = brand
        self.year = year

    def info(self):
        return f"Samochód: {self.brand} ({self.year})"
    
    def update_year(self,new_year):
        self.year = new_year
        return f"Rok dla {self.brand} zmieniono na {self.year}."

        
car1 = Car("Toyota", 1997)
car2 = Car("Skoda", 2002)
print(car1.info())
print(car2.info())

print(car1.update_year(2000))
print(car2.update_year(2011))




class User:
    def __init__(self,name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Cześć, mam na imię {self.name} i mam {self.age} lat."
    
    def update_age(self):
        self.age += 1
        return f"{self.name} ma teraz {self.age} lat!"

        
user1 = User("Robert", 43)
user2 = User("Celinka", 34)
print(user1.greet())
print(user2.greet())

print(user1.update_age())
print(user2.update_age())

class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    def add_pages(self, n):
        self.pages += n
        return f"Nowa ilość stron w książce {self.title} : {self.pages}"
    
    def __str__(self):
        return f"Książka: {self.title} autora: {self.author} ma {self.pages} stron"
    
book = Book("Titanic", "Robert", 300)
print(book)
print(book.add_pages(300))


class Account:
    def __init__(self,owner, balance):
        self.owner = owner
        self.__balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Wpłata nie może być =< od zera")
        self.__balance += amount

    def withdraw(self, amount):
        if amount > self.__balance:
            raise ValueError("brak dostępnych środków")
        if amount == self.__balance:
            return "Konto zostaje wyczyszczone ze środków"
        if amount < self.__balance:
            self.__balance -= amount
            
    def info(self):
        return f"stan środków po operacjach: {self.__balance}"
    
owner1 = Account("Robert", 1000)
owner1.deposit(100)
print(owner1.info())
owner1.withdraw(400)
print(owner1.info())

owner2 = Account("Blablabla", 500)
owner2.deposit(400)
print(owner2.info())
owner2.withdraw(100)
print(owner2.info())

class Temperature:
    def __init__(self, celsius):
        self.__celsius = celsius  # prywatny atrybut

    @property
    def celsius(self):
        """Getter – zwraca wartość w °C."""
        return self.__celsius

    @celsius.setter
    def celsius(self, value):
        """Setter – ustawia wartość w °C (np. walidacja)."""
        self.__celsius = value

    @property
    def fahrenheit(self):
        """Getter – przelicza °C na °F."""
        return (self.__celsius * 1.8) + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        """Setter – ustawia °C na podstawie podanego °F."""
        self.__celsius = (value - 32) / 1.8

    def info(self):
        """Pokazuje temperaturę w obu formatach."""
        return f"Temperatura: {self.__celsius:.1f}°C = {self.fahrenheit:.1f}°F"

temp = Temperature(100)
print(temp.info())

temp.fahrenheit = 212    # ustawia 100°C
print(temp.info())

temp.celsius = 0
print(temp.info())

#@property przy celsius → pozwala pisać temp.celsius zamiast temp.celsius()
#@celsius.setter → uruchamia się, gdy przypisujesz nową wartość
#@property przy fahrenheit → pozwala przeliczyć wartość w locie
#@fahrenheit.setter → umożliwia zapis w °F (Python sam przelicza na °C)
#__celsius → ukryty prywatny atrybut

"""
2️⃣

Zrób klasę Employee:

Atrybut __salary

Setter sprawdza, czy salary >= 4000

Getter zwraca pensję, ale tylko jeśli podano hasło (check_password())
"""
class Employee:
    def __init__(self, salary, password):
        self.__password = password
        self.__salary = salary

    def check_password(self, pwd):
        """
        Metoda porównuje wpisane hasło (pwd) z hasłem zapisanym w obiekcie.
        Używamy self._password, bo jest to hasło przypisane temu konkretnemu pracownikowi.
        """
        return pwd == self.__password
    
    def get_salary(self, pwd):
        """
        Metoda porównuje wpisane hasło (pwd) z hasłem zapisanym w obiekcie.
        Używamy self._password, bo jest to hasło przypisane temu konkretnemu pracownikowi.
        """
        if not self.check_password(pwd):
            raise PermissionError("Niepoprawne hasło")
        return self.__salary
    
    @property
    def salary(self):
        """
        Ten getter to 'czysty dostęp' do pensji BEZ autoryzacji.
        Służy np. wewnątrz programu, gdy już mamy pewność, że użytkownik ma uprawnienia.
        """
        return self.__salary
    
    @salary.setter
    def salary(self, value):
        """
        Setter pozwala zmienić pensję, ale tylko jeśli spełnia warunek: >= 4000.
        Dzięki temu nie zrobisz przypadkiem employee.salary = -1000.
        """
        if value < 4000:
            raise ValueError("Zbyt mała pensja")
        self.__salary = value
        
e = Employee(5000, "tajne")
print(e.get_salary("tajne"))   # 5000
# print(e.get_salary("zle"))   # PermissionError
e.salary = 7000                # OK (>= 4000)
# e.salary = 3500              # ValueError



