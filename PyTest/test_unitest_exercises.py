# Napisz funkcję dodaj(a, b) i przetestuj ją za pomocą unittest, sprawdzając czy dodaj(2, 3) zwraca 5.

import unittest
from unittest.mock import patch

def add(a,b):
    return a+b

class TestAddFunction(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(add(2,3),5)
#==========================================

# Zadanie: Napisz funkcję czy_parzysta(n) i przetestuj ją dla wartości parzystych i nieparzystych, używając assertTrue i assertFalse.

def czy_parzysta(n):
    return n % 2 == 0   

class TestCzy_parzysta(unittest.TestCase):
    def test_czy_parzysta(self):
        self.assertTrue(czy_parzysta(10))

    def test_czy_parzystaFalse(self):
        self.assertFalse(czy_parzysta(3))
#==========================================

# Zadanie: Napisz funkcję dziel(a, b), która rzuca ValueError, gdy b == 0. Przetestuj to za pomocą assertRaises.

def divide(a,b):
    if b == 0:
        raise ValueError("Nie dzielimy przez zero")
    return a / b

class Testdvidion(unittest.TestCase):
    def test_divide(self):
        with self.assertRaises(ValueError):
            divide(2,0)

    def test_divide_ok(self):
        self.assertEqual(divide(8,2),4)
#=========================================

# Zadanie: Zbuduj klasę Kalkulator z metodą dodaj(x), która dodaje wartość do wewnętrznego pola wynik. Przetestuj ją, używając setUp() i assertEqual.

class Calc:
    def __init__(self,wynik):
        self.wynik = wynik

    def dodaj(self,x):
            return self.wynik+x

#calc = Calc(10)
#print(calc.dodaj(10))

class TestCalc(unittest.TestCase):
    def setUp(self):
        self.calc = Calc(10)

    def test_dodaj(self):
        self.assertEqual(self.calc.dodaj(10),20)

    def tearDown(self):
        print("Test zakończony")
#=========================================


# Masz funkcję pobierz_dane(), która zwraca dane z zewnętrznego źródła (np. API). Funkcja przetworz() bierze te dane i coś z nimi robi — 
# np. zamienia na wielkie litery.
# 🎯 Cel testu:
# Sprawdzić, czy przetworz() działa poprawnie niezależnie od tego, co zwraca pobierz_dane() — czyli podmienić ją na wartość testową.

# 🧩 Twoje zadanie:
# - Napisz funkcję pobierz_dane(), która zwraca np. "prawdziwe dane".
# - Napisz funkcję przetworz(), która pobiera dane i zwraca je jako wielkie litery.
# - Napisz test, który używa unittest.mock.patch, żeby podmienić pobierz_dane() na "test" i sprawdzić, czy przetworz() zwraca "TEST".


def pobierz_dane():
    return "Teoretycznie prawdziwe dane"
    

def przetworz():
    dane = pobierz_dane()
    return dane.upper()

class TestowaniePobierania(unittest.TestCase):
    @patch("__main__.pobierz_dane")

    def test_przetworz(self, mock_api):
        mock_api.return_value = "testowe sztuczne dane"
        wynik = przetworz()
        self.assertEqual(wynik, "TESTOWE SZTUCZNE DANE")
        mock_api.assert_called_once()
#=========================================


# 🧪 Ćwiczenie 6: Testowanie funkcji rzucającej wyjątek
# Napisz test, który sprawdza, czy dziel(10, 0) rzuca wyjątek ValueError

def dziel(a, b):
    if b == 0:
        raise ValueError("Nie dzielimy przez zero")
    return a / b

class TestsDzielFunction(unittest.TestCase):
    def test_dziel(self):
        with self.assertRaises(ValueError):
            dziel(5,0)


    def test_dziel_ok(self):
        self.assertEqual(dziel(10,2),5)
#=========================================


# 🧪 Ćwiczenie 7: Testowanie klasy z wieloma metodami
# Napisz test, który sprawdza czy po wpłacie 100 saldo wynosi 100

class BankKonto:
    def __init__(self):
        self._saldo = 0

    def wplac(self, kwota):
        self._saldo += kwota

    def saldo(self):
        return self._saldo

class TestBankKonto(unittest.TestCase):

    def setUp(self):
        self.bank = BankKonto()
    
    def test_wplac(self):
        self.bank.wplac(100)
        self.assertEqual(self.bank.saldo(),100)


#=========================================


# 🧪 Ćwiczenie 8: Testowanie listy wyników
# Napisz test, który sprawdza czy wynik zawiera tylko liczby parzyste

def filtruj_parzyste(lista):
    return [x for x in lista if x % 2 == 0]

class TestFiltruj(unittest.TestCase):
    def test_filtruj_parzyste(self):
        self.assertEqual(filtruj_parzyste([1,2,3,4,5,6,7,8,9,10]),[2,4,6,8,10])
        self.assertEqual(filtruj_parzyste([]),[])
        self.assertEqual(filtruj_parzyste(1,3,5),[]) # - tu test nie przechodzi, założenia funkcji są oczywiście inne.


#=========================================



# 🧪 Ćwiczenie 9: Testowanie porównania obiektów
# Napisz test, który porównuje dwie osoby i sprawdza czy są równe lub różne

class Osoba:
    def __init__(self, imie, wiek):
        self.imie = imie
        self.wiek = wiek

    def __eq__(self, other):
        return self.imie == other.imie and self.wiek == other.wiek


class TestOsoba(unittest.TestCase):
    def setUp(self):
        self.osoba = Osoba("Robert",43)

    def test_eq(self):
        inna_osoba = Osoba("Robert",43)
        self.assertEqual(self.osoba, inna_osoba)

    def test_eq_Fail(self):
        inna_osoba = Osoba("Michał", 23)
        self.assertEqual(self.osoba, inna_osoba) # - tu test nie przejdzie, porównanie nie jest True


#=========================================



# 🧪 Ćwiczenie 10: Testowanie funkcji z parametrami wejściowymi
# Napisz test z subTest(), który sprawdza obliczanie podatku dla różnych stawek

def oblicz_podatek(kwota, stawka):
    return kwota * stawka

class Test_oblicz_podatek_SubTest(unittest.TestCase):
    
    def test_oblicz_podatki(self):
        przypadki = [(100,1.23,123),(50,0.8,40),(10,1.10,11),(0,0,0)]
        for kwota,stawka, wynik in przypadki:
            with self.subTest(kwota=kwota, stawka=stawka):
                self.assertEqual(oblicz_podatek(kwota,stawka),wynik)


#=========================================
# 🧪 Ćwiczenie 16: Testowanie metody __str__ w klasie
# Napisz klasę Film z polami tytuł i rok oraz metodą __str__ zwracającą opis filmu.
# Przetestuj, czy str(Film("Matrix", 1999)) zwraca "Film: Matrix (1999)"

class Film:
    def __init__(self,title,year):
        self.title = title
        self.year = year

    def __str__(self):
        return f"Film: {self.title} ({self.year})"
    
class TestFilm(unittest.TestCase):
    def setUp(self):
        self.film = Film("Matrix",1999)


    def test_film(self):
        self.assertEqual(str(self.film), "Film: Matrix (1999)")
        






#=========================================
# 🧪 Ćwiczenie 17: Testowanie metody zmieniającej stan obiektu
# Napisz klasę Licznik z metodą zwieksz(), która zwiększa licznik o 1.
# Przetestuj, czy po trzech wywołaniach licznik wynosi 3.
#=========================================
# 🧪 Ćwiczenie 18: Testowanie wyjątku w klasie
# Napisz klasę Konto z metodą wyplac(kwota), która rzuca wyjątek jeśli saldo jest za małe.
# Przetestuj, czy wyplac(100) rzuca wyjątek przy saldzie 50.
#=========================================
# 🧪 Ćwiczenie 19: Testowanie listy obiektów
# Napisz klasę Produkt z polem nazwa. Stwórz funkcję filtruj_po_nazwie(lista, litera), która zwraca produkty zaczynające się od litery.
# Przetestuj, czy filtracja działa poprawnie dla listy obiektów.
#=========================================
# 🧪 Ćwiczenie 20: Testowanie zaokrąglania
# Napisz funkcję zaokraglij(x), która zwraca x zaokrąglone do dwóch miejsc po przecinku.
# Przetestuj ją dla różnych wartości używając assertAlmostEqual()
#=========================================

if __name__ == "__main__":
    unittest.main()