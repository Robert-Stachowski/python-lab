"""
=============================================================
 PYTHON CHEATSHEET: sum(), any(), all()
=============================================================
Autor: Robert Stachowski + ChatGPT mentoring
Cel: Poznać i zrozumieć trzy potężne funkcje Pythona:
      - sum()
      - any()
      - all()
Opis:
  - jak działają
  - kiedy i gdzie ich używać
  - wzorce użycia (patterns)
  - pułapki i dobre praktyki
=============================================================
"""

# ------------------------------------------------------------
# 1) sum(iterable, start=0)
# ------------------------------------------------------------
# Funkcja sumuje elementy iterowalne (np. liczby, wartości logiczne).
# Gdy elementy są typu bool, True = 1, False = 0.
# Idealna do liczenia warunków lub sumowania przekształconych wartości.

# Klasyczny przykład: ile liczb parzystych w przedziale 0–9
parzyste = sum(n % 2 == 0 for n in range(10))  # True==1, False==0 → wynik 5
print("Parzyste:", parzyste)

# Liczenie cyfr i liter w stringu
tekst = "A1b2C3"
digits  = sum(ch.isdigit() for ch in tekst)  # 3
letters = sum(ch.isalpha() for ch in tekst)  # 3
print("Cyfry:", digits, "| Litery:", letters)

# Sumowanie przekształconych liczb: kwadraty parzystych
suma_kwadratow = sum(n * n for n in range(10) if n % 2 == 0)
print("Suma kwadratów parzystych:", suma_kwadratow)

# Policzenie trafień z użyciem 1 dla czytelności
podzielne_przez_3 = sum(1 for n in range(30) if n % 3 == 0)
print("Podzielne przez 3:", podzielne_przez_3)

# ------------------------------------------------------------
# 2) any(iterable)
# ------------------------------------------------------------
# Zwraca True, jeśli chociaż jeden element jest „prawdziwy”.
# Idealna do sprawdzenia: „czy istnieje przynajmniej jeden przypadek?”
# Działa z leniwym sprawdzaniem – zatrzymuje się na pierwszym True.

numbers = [1, -5, 0, 3]
ma_ujemne = any(n < 0 for n in numbers)  # True (bo -5)
print("Czy są liczby ujemne?", ma_ujemne)

# Czy w nazwach plików jest coś z rozszerzeniem .py?
filenames = ["test.txt", "main.py", "notes.md"]
ma_py = any(name.endswith(".py") for name in filenames)
print("Czy istnieje plik .py?", ma_py)

# Czy w haśle jest jakikolwiek znak specjalny?
password = "Hello@123"
specials = set("!@#$%^&*")
ma_specjalny = any(ch in specials for ch in password)
print("Hasło ma znak specjalny?", ma_specjalny)

# Walidacja danych: czy występuje None?
payload = [12, 45, None, 7]
if any(x is None for x in payload):
    print("⚠️  Brakuje wartości w danych!")

# ------------------------------------------------------------
# 3) all(iterable)
# ------------------------------------------------------------
# Zwraca True, jeśli wszystkie elementy są „prawdziwe”.
# Idealna do sprawdzania poprawności formatu lub jednolitości danych.
# Zatrzymuje się na pierwszym False.

numbers = [1, 2, 3, 4]
same_dodatnie = all(n > 0 for n in numbers)
print("Wszystkie liczby dodatnie?", same_dodatnie)

# Sprawdź, czy promo code zawiera wyłącznie DUŻE litery i cyfry
code = "ABC123XYZ0"
format_ok = all(ch.isupper() or ch.isdigit() for ch in code)
print("Format kodu poprawny?", format_ok)

# Czy wszystkie wiersze CSV mają tę samą długość?
rows = [
    ["ID", "Name", "Age"],
    ["1", "Ala", "25"],
    ["2", "Robert", "29"],
]
row_lengths = (len(row) for row in rows)
pierwsza = len(rows[0])
spojne = all(length == pierwsza for length in row_lengths)
print("Czy wszystkie wiersze mają tę samą długość?", spojne)

# ------------------------------------------------------------
# 4) Kombinacje walidacyjne
# ------------------------------------------------------------
# Najczęściej spotykane połączenia any/all/sum w walidacjach

code = "AB12C3XYZ9"

# 1) tylko DUŻE litery i cyfry
if not all(ch.isupper() or ch.isdigit() for ch in code):
    print("Kod zawiera niedozwolone znaki!")

# 2) co najmniej dwie cyfry
if sum(ch.isdigit() for ch in code) < 2:
    print("Kod musi mieć co najmniej 2 cyfry!")

# 3) musi mieć przynajmniej jedną literę i jedną cyfrę
if not any(ch.isalpha() for ch in code):
    print("Brakuje liter!")
if not any(ch.isdigit() for ch in code):
    print("Brakuje cyfr!")

# 4) jednolinijkowy warunek logiczny
is_ok = (
    isinstance(code, str)
    and len(code) == 10
    and all(ch.isupper() or ch.isdigit() for ch in code)
    and sum(ch.isdigit() for ch in code) >= 2
)
print("Kod poprawny:", is_ok)

# ------------------------------------------------------------
# 5) Przykłady z range()
# ------------------------------------------------------------

# Ile liczb parzystych w zakresie 0–99?
parzyste = sum(n % 2 == 0 for n in range(100))
print("Parzyste (0–99):", parzyste)

# Czy jakakolwiek liczba > 90?
jest_duza = any(n > 90 for n in range(100))
print("Czy >90 istnieje?", jest_duza)

# Czy wszystkie liczby < 100?
wszystkie_mniejsze = all(n < 100 for n in range(100))
print("Czy wszystkie <100?", wszystkie_mniejsze)

# ------------------------------------------------------------
# 6) Listy, słowniki, pliki
# ------------------------------------------------------------

nums = [3, -1, 5, 0]
ma_zero = any(n == 0 for n in nums)
same_dodatnie = all(n > 0 for n in nums)
print("Zawiera zero?", ma_zero, "| Wszystkie dodatnie?", same_dodatnie)

d = {"user_id": 1, "name": "Ala"}
ma_user_klucz = any(k.startswith("user_") for k in d)
print("Czy jest klucz user_*?", ma_user_klucz)

paths = ["file1.txt", "notes.txt", "readme.md"]
only_txt = all(path.endswith(".txt") for path in paths)
print("Czy wszystkie to .txt?", only_txt)

# ------------------------------------------------------------
# 7) Testy jednostkowe (pytest style)
# ------------------------------------------------------------
# any/all/sum idealnie nadają się do asercji warunków logicznych

def test_has_at_least_two_digits():
    assert sum(ch.isdigit() for ch in "AB12XYZ9Q") >= 2

def test_only_upper_and_digits():
    assert all(ch.isupper() or ch.isdigit() for ch in "ABC123XYZ0")

def test_any_negative_in_payload():
    data = [1, 2, -3, 4]
    assert any(n < 0 for n in data)

# ------------------------------------------------------------
# 8) Szybki przewodnik: kiedy co używać
# ------------------------------------------------------------
# sum() → licz, ile przypadków (True==1)
# any() → czy istnieje choć jeden przypadek?
# all() → czy wszystkie spełniają warunek?

# Przykład:
numbers = [1, 0, -2, 5, 7]

# 1) Ile liczb dodatnich?
print("Dodatnie:", sum(n > 0 for n in numbers))

# 2) Czy jest liczba ujemna?
print("Ma ujemne:", any(n < 0 for n in numbers))

# 3) Czy wszystkie > 0?
print("Wszystkie dodatnie:", all(n > 0 for n in numbers))

# ------------------------------------------------------------
# 9) Pułapki i dobre praktyki
# ------------------------------------------------------------
# - any([]) == False, all([]) == True  → tzw. „pusta prawda”
# - używaj generatorów: sum(x for x in ...) zamiast list: sum([x for x in ...])
# - sum() na boolach = liczba trafień
# - „i litera, i cyfra” → dwa any():
#     any(ch.isalpha() for ch in s) and any(ch.isdigit() for ch in s)
# - odrzucaj błędy przez not all()/sum()<X  – to czytelny wzorzec w walidacjach

# ------------------------------------------------------------
# KONIEC
# ------------------------------------------------------------
