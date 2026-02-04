# 📘 Ściąga: Testy jednostkowe w Pythonie z unittest

import unittest
from unittest.mock import patch

# 🔹 Funkcja, którą testujemy
def suma(a, b):
    return a + b

# 🔹 Klasa testowa dziedzicząca po unittest.TestCase
class TestSuma(unittest.TestCase):

    # 🔸 Test 1: Dodawanie dwóch dodatnich liczb
    def test_dodawanie_liczb_dodatnich(self):
        self.assertEqual(suma(2, 3), 5)

    # 🔸 Test 2: Dodawanie liczby ujemnej i dodatniej
    def test_dodawanie_ujemnej_i_dodatniej(self):
        self.assertEqual(suma(-2, 5), 3)

    # 🔸 Test 3: Dodawanie zera
    def test_dodawanie_zer(self):
        self.assertEqual(suma(0, 0), 0)

    # 🔸 Test 4: Dodawanie dużych liczb
    def test_dodawanie_duzych_liczb(self):
        self.assertEqual(suma(1000000, 2000000), 3000000)

# 🔹 Uruchamianie testów na samym dole, tylko jeden __main__ na plik!


#=================================================================

# 📘 Ściąga: Testowanie wyjątków i klas z metodami w unittest



# 🔹 Funkcja z wyjątkiem
def dziel(a, b):
    if b == 0:
        raise ValueError("Nie można dzielić przez zero")
    return a / b

# 🔹 Klasa z metodami
class Kalkulator:
    def dodaj(self, a, b):
        return a + b

    def odejmij(self, a, b):
        return a - b

    def pomnoz(self, a, b):
        return a * b

    def podziel(self, a, b):
        if b == 0:
            raise ValueError("Dzielenie przez zero")
        return a / b

# 🔹 Testy funkcji dziel
class TestDziel(unittest.TestCase):
    def test_poprawne_dzielenie(self):
        self.assertEqual(dziel(10, 2), 5)

    def test_dzielenie_przez_zero(self):
        with self.assertRaises(ValueError):
            dziel(10, 0)

# 🔹 Testy klasy Kalkulator
class TestKalkulator(unittest.TestCase):

    def setUp(self):
        self.kalk = Kalkulator()

    def test_dodaj(self):
        self.assertEqual(self.kalk.dodaj(3, 4), 7)

    def test_odejmij(self):
        self.assertEqual(self.kalk.odejmij(10, 5), 5)

    def test_pomnoz(self):
        self.assertEqual(self.kalk.pomnoz(2, 3), 6)

    def test_podziel(self):
        self.assertEqual(self.kalk.podziel(8, 2), 4)

    def test_podziel_przez_zero(self):
        with self.assertRaises(ValueError):
            self.kalk.podziel(5, 0)

    def tearDown(self):
        print("Test zakończony")

# 🔹 Uruchamianie testów na samym dole, tylko jeden __main__ na plik!


#==========================================================================

# 📘 Ściąga: Mockowanie w unittest z użyciem unittest.mock
# 🔍 Cel: Zastąpienie prawdziwej funkcji sztuczną (mockowaną), by testować logikę bez zależności zewnętrznych



# 🔹 Funkcja, która normalnie pobiera dane z zewnętrznego źródła (np. API)
def pobierz_dane_z_api():
    # Tu byłby np. request do zewnętrznego serwera
    raise NotImplementedError("To tylko symulacja — nie mamy prawdziwego API")

# 🔹 Funkcja, którą chcemy przetestować — korzysta z danych z API
def przetworz_dane():
    dane = pobierz_dane_z_api()  # <- zależność zewnętrzna
    return dane.upper()          # <- logika, którą chcemy testować

# 🔹 Test z mockowaniem funkcji pobierz_dane_z_api
class TestMockowanie(unittest.TestCase):

    # 🔸 Dekorator @patch podmienia funkcję pobierz_dane_z_api na sztuczną wersję (mock)
    @patch('__main__.pobierz_dane_z_api')  # <- ścieżka do funkcji, którą mockujemy
    def test_przetworz_dane(self, mock_api):
        # 🔸 Ustawiamy, co ma zwrócić mockowana funkcja
        mock_api.return_value = 'testowe dane'

        # 🔸 Wywołujemy funkcję, która korzysta z mocka
        wynik = przetworz_dane()

        # 🔸 Sprawdzamy, czy wynik jest zgodny z oczekiwanym
        self.assertEqual(wynik, 'TESTOWE DANE')

        # 🔸 Sprawdzamy, czy mockowana funkcja została wywołana dokładnie raz
        mock_api.assert_called_once()

# 🔹 Uruchamianie testów na samym dole.


# 🧠 Co tu się dzieje — krok po kroku:
# - Problem: Funkcja przetworz_dane() korzysta z pobierz_dane_z_api(), której nie chcemy uruchamiać w testach (bo np. łączy się z internetem).
# - Rozwiązanie: Używamy @patch, by podmienić prawdziwą funkcję na sztuczną (mock).
# - mock_api.return_value — ustalamy, co ma zwrócić mock zamiast prawdziwego API.
# - Testujemy tylko logikę przetworz_dane(), bez zależności zewnętrznych.
# - assert_called_once() — upewniamy się, że mockowana funkcja została wywołana.


#=======================================================================

# 📘 Ściąga: Najważniejsze metody asercji w unittest (Python)



# 🔹 Funkcje pomocnicze do testów
def suma(a, b):
    return a + b

def dziel(a, b):
    if b == 0:
        raise ValueError("Nie można dzielić przez zero")
    return a / b

def pobierz_role_uzytkownika():
    return ['user', 'editor']

class TestAsercje(unittest.TestCase):

    # 🔸 assertEqual — sprawdza, czy dwa wartości są równe
    def test_assert_equal(self):
        self.assertEqual(suma(2, 3), 5)

    # 🔸 assertTrue — sprawdza, czy wartość jest True
    def test_assert_true(self):
        self.assertTrue(10 > 5)

    # 🔸 assertFalse — sprawdza, czy wartość jest False
    def test_assert_false(self):
        self.assertFalse(3 > 5)

    # 🔸 assertIsNone — sprawdza, czy wartość to None
    def test_assert_is_none(self):
        wynik = None
        self.assertIsNone(wynik)

    # 🔸 assertIsInstance — sprawdza typ obiektu
    def test_assert_is_instance(self):
        self.assertIsInstance("tekst", str)

    # 🔸 assertIn — sprawdza, czy element znajduje się w kolekcji
    def test_assert_in(self):
        role = pobierz_role_uzytkownika()
        self.assertIn('editor', role)

    # 🔸 assertNotIn — sprawdza, czy element NIE znajduje się w kolekcji
    def test_assert_not_in(self):
        role = pobierz_role_uzytkownika()
        self.assertNotIn('admin', role)

    # 🔸 assertRaises — sprawdza, czy funkcja rzuca wyjątek
    def test_assert_raises(self):
        with self.assertRaises(ValueError):
            dziel(10, 0)

# 🔹 Uruchamianie testów na samym dole


# 🧠 Co warto zapamiętać:
# - Asercje to serce testów — każda sprawdza inny typ zachowania.
# - assertRaises i assertNotIn są szczególnie ważne w testach bezpieczeństwa i walidacji.
# - Możesz używa

#================================================================================

# 📘 Ściąga: subTest() w unittest — testowanie wielu przypadków w jednej metodzie



# 🔹 Funkcja, którą testujemy
def suma(a, b):
    return a + b

class TestSubTest(unittest.TestCase):

    # 🔸 Test z wieloma przypadkami przy użyciu subTest()
    def test_wiele_przypadkow_suma(self):
        przypadki = [
            (2, 3, 5),
            (0, 0, 0),
            (-1, 1, 0),
            (100, 200, 300),
            (-5, -5, -10)
        ]

        for a, b, oczekiwany in przypadki:
            # 🔸 subTest tworzy osobny kontekst dla każdego przypadku
            with self.subTest(a=a, b=b):
                self.assertEqual(suma(a, b), oczekiwany)


# 🧠 Co warto wiedzieć o subTest():
# - ✅ Każdy przypadek jest traktowany osobno — jeśli jeden zawiedzie, reszta nadal się wykonuje.
# - ✅ W raporcie testów zobaczysz, który przypadek się nie powiódł — z podanymi wartościami a i b.
# - ✅ To idealne rozwiązanie do testowania funkcji z wieloma zestawami danych (np. walidacje, obliczenia, formatowanie).
#
# 📌 Kiedy używać subTest()?
# - Gdy masz wiele podobnych przypadków do przetestowania.
# - Gdy chcesz zachować czytelność kodu testowego.
# - Gdy nie chcesz pisać osobnych metod testowych dla każdego zestawu danych.
#=============================================================================================================
#=============================================================================================================
#=============================================================================================================
#=============================================================================================================
import unittest

# 🔧 Przykładowe funkcje do testowania
def dodaj(a, b):
    return a + b

def dziel(a, b):
    if b == 0:
        raise ValueError("Nie dzielimy przez zero")
    return a / b

def czy_parzysta(n):
    return n % 2 == 0

def typ_danych(x):
    return type(x).__name__

# 🔧 Przykładowa klasa
class Kalkulator:
    def __init__(self):
        self.wynik = 0

    def dodaj(self, x):
        self.wynik += x
        return self.wynik

    def odejmij(self, x):
        self.wynik -= x
        return self.wynik

    def saldo(self):
        return self.wynik

# 🧪 Kompendium testów
class TestWzorceUnittest(unittest.TestCase):

    # 🔹 setUp — przygotowanie obiektu przed każdym testem
    def setUp(self):
        self.kalk = Kalkulator()

    # 🔹 assertEqual — porównanie wartości
    def test_dodaj(self):
        self.assertEqual(dodaj(2, 3), 5)

    # 🔹 assertTrue / assertFalse — sprawdzanie warunku logicznego
    def test_parzysta(self):
        self.assertTrue(czy_parzysta(4))
        self.assertFalse(czy_parzysta(5))

    # 🔹 assertRaises — sprawdzanie wyjątku
    def test_dziel_przez_zero(self):
        with self.assertRaises(ValueError):
            dziel(10, 0)

    # 🔹 assertIn / assertNotIn — sprawdzanie obecności w kolekcji
    def test_lista_elementow(self):
        lista = [1, 2, 3]
        self.assertIn(2, lista)
        self.assertNotIn(5, lista)

    # 🔹 assertIsInstance — sprawdzanie typu
    def test_typ_danych(self):
        self.assertEqual(typ_danych(123), "int")
        self.assertEqual(typ_danych("abc"), "str")

    # 🔹 subTest — testowanie wielu przypadków w jednej metodzie
    def test_dodawanie_wielu(self):
        przypadki = [(1, 2, 3), (0, 0, 0), (-1, 1, 0)]
        for a, b, wynik in przypadki:
            with self.subTest(a=a, b=b):
                self.assertEqual(dodaj(a, b), wynik)

    # 🔹 testowanie stanu klasy po operacjach
    def test_saldo_po_operacjach(self):
        self.kalk.dodaj(100)
        self.kalk.odejmij(40)
        self.assertEqual(self.kalk.saldo(), 60)

    # 🔹 tearDown — sprzątanie po teście (opcjonalne)
    def tearDown(self):
        print("Test zakończony")

# 🔹 Uruchomienie testów
if __name__ == "__main__":
    unittest.main()