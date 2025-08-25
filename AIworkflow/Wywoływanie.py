# Python – ściąga: kiedy używać (), [] i .

## 1. Nawiasy okrągłe `()` – WYWOŁYWANIE
- Służą do URUCHAMIANIA (wywoływania) funkcji, metod, klas.
- Myśl: „ODPALAM coś”.
- Przykłady:
    print("Hello")             # funkcja wbudowana
    len([1, 2, 3])             # funkcja wbudowana
    user_input = input()       # funkcja wbudowana

- Funkcje własne:
    def powitanie(imie):
        return f"Cześć {imie}!"
    print(powitanie("Robert"))

- Klasy i metody:
    class Dog:
        def __init__(self, name):
            self.name = name
        def bark(self):
            return f"{self.name} szczeka!"

    pies = Dog("Reksio")       # wywołanie klasy (tworzenie obiektu)
    print(pies.bark())         # metoda obiektu (z nawiasami)

**Zapamiętaj:**  
- Funkcja: nazwa_funkcji()  
- Metoda: obiekt.metoda()  
- Klasa (obiekt): NazwaKlasy()  

---

## 2. Nawiasy kwadratowe `[]` – DOSTĘP DO ELEMENTÓW
- Służą do POBIERANIA elementów z list, krotek, stringów lub wartości w słowniku.
- Myśl: „WYCIĄGAM coś ze środka”.
- Przykłady:
    lista = [10, 20, 30]
    print(lista[0])         # 10 (pierwszy element)

    napis = "Python"
    print(napis[2])         # 't' (trzeci znak)

    slownik = {"a": 1, "b": 2}
    print(slownik["a"])     # 1 (wartość dla klucza "a")

---

## 3. Slicing (też z `[]`) – FRAGMENTY
- Pobieranie części listy, stringa, itp.
- Przykłady:
    lista = [0, 1, 2, 3, 4, 5]
    print(lista[1:4])       # [1, 2, 3] – od indeksu 1 do 3
    print(lista[:3])        # [0, 1, 2] – od początku do indeksu 2
    print(lista[3:])        # [3, 4, 5] – od indeksu 3 do końca
    print(lista[::2])       # [0, 2, 4] – co drugi element

---

## 4. Kropka `.` – DOSTĘP DO ATRYBUTÓW I METOD
- Służy do sięgania „do środka obiektu”.
- Może oznaczać:
    - Atrybut (dane, cecha obiektu) – bez nawiasów.
    - Metodę (funkcja obiektu) – z nawiasami, bo wywołujesz.
- Przykłady:
    tekst = "python"
    print(tekst.upper())       # metoda (wszystkie litery duże)
    print(tekst.capitalize())  # metoda (pierwsza litera duża)

    class User:
        def __init__(self, name):
            self.name = name
        def hello(self):
            return f"Cześć, {self.name}!"

    u = User("Robert")
    print(u.name)              # atrybut – odczyt
    print(u.hello())           # metoda – wywołanie

---

## 5. Typowe błędy
- Próba użycia złych nawiasów:
    square = {x: x**2 for x in [1, 2, 3]}
    print(square(2))   # ❌ Błąd: 'dict' object is not callable
    print(square[2])   # ✅ Poprawnie -> 4

---

## 6. Jak zapamiętać?
- **`()`** – coś WYWOŁUJĘ (funkcja, metoda, klasa).  
- **`[]`** – coś WYCIĄGAM (element, klucz, fragment).  
- **`.`** – WCHODZĘ DO OBIEKTU (po dane lub metodę).  

---
