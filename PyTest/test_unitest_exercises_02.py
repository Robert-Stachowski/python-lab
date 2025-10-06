# ============================================
# 🧪 ZESTAW ĆWICZEŃ UNITTEST – ROBERT EDITION
# Zakres: assertAlmostEqual, assertIn, assertNotIn,
# assertRaises, assertIsNone, assertIsInstance,
# slicing, os, sys, mock (@patch)
# ============================================

# 1️⃣ assertAlmostEqual – średnia z dokładnością
# ------------------------------------------------
# Napisz funkcję avg(nums), która zwraca średnią arytmetyczną.
# Przetestuj ją dla kilku list (z int i float).
# Użyj assertAlmostEqual(..., places=2) oraz subTest.
# Dodaj przypadek graniczny z zaokrągleniem np. 2.675.
# TODO

import unittest

def avg(nums):
    return sum(nums)/len(nums)

nums = [
    (1,2,3),
    (3,4.8,5,6),
    (1.1,1)
    ]
wynik = [avg([*x]) for x in nums]
print(f"{wynik}\n")
for group in nums:
    print(f"{avg([*group])}\n")


class TestAvg(unittest.TestCase):
    def test_avg(self):
        test1 = (1,2,7,3)
        test2 = (1,2,5,3)
        test3 = (1,2,3,3)
        self.assertAlmostEqual(avg([*test1]), 3.25)
        self.assertAlmostEqual(avg([*test2]), 2.75)
        self.assertAlmostEqual(avg([*test3]), 2.25)

    def test_avg_SubTest(self):
        przypadki = [
            ([1,1,1,2.3],1.325),
            ([2,3,4,5],3.5),
            ([4,4,4,4.3],4.075)
        ]
        for group, wyjscie in przypadki:
            with self.subTest(group=group):
                self.assertAlmostEqual(avg(group),wyjscie, places=2)

    def test_avg_SubTest_error(self):
        przypadki_error = [
            ([1,1,1],5),
            ([2,2,2],7),
            ([3,3,3],9.1)
        ]
        for group, wynik in przypadki_error:
            with self.subTest(group=group):
                self.assertAlmostEqual(avg(group), wynik, places=2, msg="Celowe oblanie testów!")





# 2️⃣ assertIn / assertNotIn – filtrowanie nazw
# ------------------------------------------------
# Funkcja filter_prefix(items, prefix) zwraca nazwy
# zaczynające się na prefix (case-insensitive).
# Testy:
#  - assertIn("Awokado", wynik)
#  - assertNotIn("Młynek", wynik)
#  - assertEqual(len(wynik), 2)
#  - Bonus: assertCountEqual(wynik, ["Awokado", "Awionetka"])

# TODO


# 3️⃣ assertRaises (+ komunikat) – walidacja płatności
# ------------------------------------------------
# Klasa Wallet(balance) z metodą pay(amount).
# Jeśli amount > balance → raise ValueError("insufficient funds").
# Testy:
#  - assertRaises(ValueError)
#  - assertIn("insufficient", str(context.exception))

# TODO


# 4️⃣ assertIsNone / assertIsNotNone – wyszukiwarka
# ------------------------------------------------
# Funkcja find_user(users, username) zwraca obiekt użytkownika
# lub None, jeśli nie istnieje.
# Testy:
#  - assertIsNotNone dla istniejącego
#  - assertIsNone dla nieistniejącego
#  - Bonus: assertEqual(result.name, "Robert")

# TODO


# 5️⃣ assertIsInstance – prosta fabryka obiektów
# ------------------------------------------------
# Funkcja make_product(name, price) zwraca instancję klasy Product.
# Testy:
#  - assertIsInstance(obj, Product)
#  - assertEqual(obj.name, ...)
#  - assertAlmostEqual(obj.price, ..., places=2)

# TODO


# 6️⃣ Slicing – wycinek danych
# ------------------------------------------------
# Funkcja middle_slice(seq, start, stop, step=1)
# zwraca wycinek seq[start:stop:step].
# Testy:
#  - różne warianty: pozytywne/negatywne indeksy, step>1
#  - assertEqual(middle_slice([], 0, 1), [])
#  - assertEqual(middle_slice("abcdef", None, None, 2), "ace")

# TODO


# 7️⃣ os – praca na plikach w katalogu
# ------------------------------------------------
# Funkcja list_txt_files(dir_path) → lista nazw plików .txt w katalogu (posortowana).
# Test:
#  - utwórz katalog tymczasowy
#  - stwórz 3–4 pliki, w tym 2 .txt
#  - assertEqual(result, ["a.txt", "b.txt"])
#  - pusty katalog → []

# Wskazówki:
#  - użyj tempfile.TemporaryDirectory()
#  - os.path.join() do tworzenia ścieżek
#  - po teście katalog sam się usunie

# TODO


# 8️⃣ sys – parsowanie argumentów
# ------------------------------------------------
# Funkcja parse_args(args) przyjmuje np. ["--mode", "fast", "--limit", "10"]
# i zwraca dict z {"mode": "fast", "limit": 10}.
# Testy:
#  - assertEqual(parsed["mode"], "fast")
#  - assertEqual(parsed["limit"], 10)
#  - brak argumentów → assertRaises(ValueError)
#  - subTest dla wielu zestawów

# TODO


# 9️⃣ Mockowanie (@patch) – pobieranie JSON
# ------------------------------------------------
# Funkcja fetch_json(url) używa requests.get(url).json() i zwraca dict.
# Testy (z dekoratorem @patch):
#  - zamokuj requests.get tak, by .json() zwróciło {"ok": True}
#  - assertEqual(fetch_json("http://x"), {"ok": True})
#  - requests.get.assert_called_once_with("http://x")
#  - Bonus: test błędu → assertRaises

# TODO


# 🔟 Integracja – plik → obliczenia → wynik
# ------------------------------------------------
# Funkcja sum_prices_from_file(path) czyta CSV: name,price
# i zwraca sumę zaokrągloną do 2 miejsc.
# Testy:
#  - użyj tymczasowego pliku (tempfile.NamedTemporaryFile)
#  - assertAlmostEqual(suma, oczekiwana, places=2)
#  - pusty plik → 0.00
#  - błędny wiersz → assertRaises(ValueError)

# TODO

if __name__ == "__main__":
    unittest.main(verbosity=2)
