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
class BankKonto:
    def __init__(self):
        self._saldo = 0

    def wplac(self, kwota):
        self._saldo += kwota

    def saldo(self):
        return self._saldo

# Napisz test, który sprawdza czy po wpłacie 100 saldo wynosi 100
#=========================================





# 🧪 Ćwiczenie 8: Testowanie listy wyników
def filtruj_parzyste(lista):
    return [x for x in lista if x % 2 == 0]

# Napisz test, który sprawdza czy wynik zawiera tylko liczby parzyste
#=========================================





# 🧪 Ćwiczenie 9: Testowanie porównania obiektów
class Osoba:
    def __init__(self, imie, wiek):
        self.imie = imie
        self.wiek = wiek

    def __eq__(self, other):
        return self.imie == other.imie and self.wiek == other.wiek

# Napisz test, który porównuje dwie osoby i sprawdza czy są równe lub różne
#=========================================






# 🧪 Ćwiczenie 10: Testowanie funkcji z parametrami wejściowymi
def oblicz_podatek(kwota, stawka):
    return kwota * stawka

# Napisz test z subTest(), który sprawdza obliczanie podatku dla różnych stawek
#=========================================



if __name__ == "__main__":
    unittest.main()