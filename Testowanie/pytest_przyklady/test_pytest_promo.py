import pytest
from pytest_promo import is_valid_promo, is_valid_promo_and

@pytest.mark.parametrize("func", [is_valid_promo,is_valid_promo_and])
@pytest.mark.parametrize("code, expected",
[
("ABC123XY90", True),
("ABCDEFGH12", True),
("QWERTYUIOP12", False),
("AB123", False),
("abc123defg", False),
("ABCDEFGHIJ",False),
(1234567890,False),
("ABC!@#123$",False),
])
def test_is_valid_promo_functions(func,code,expected):
    assert func(code) == expected

# ==============================================================
# 
# ==============================================================
# 1️⃣ Importujemy pytest oraz dwie funkcje z pliku pytest_promo.py:
#     - is_valid_promo      → wersja "normalna" z if-ami
#     - is_valid_promo_and  → wersja skrócona z łańcuchem and
#
# 2️⃣ Dekorator @pytest.mark.parametrize("func", [...])
#     - pytest sam "wstrzykuje" każdą funkcję z listy jako argument func.
#     - Dzięki temu test uruchomi się osobno dla:
#          a) is_valid_promo
#          b) is_valid_promo_and
#
# 3️⃣ Drugi dekorator @pytest.mark.parametrize("code, expected", [...])
#     - definiuje zestaw danych testowych (parametry wejściowe i oczekiwany wynik)
#     - Każdy kod promocyjny (code) ma być sprawdzony, czy jest poprawny (True/False)
#
# 4️⃣ Pytest wykonuje testy kombinacyjnie:
#        liczba_funkcji * liczba_danych = 2 * 8 = 16 testów
#
# 5️⃣ Funkcja test_is_valid_promo_functions(func, code, expected)
#     - pytest podstawia tu po kolei wszystkie wartości z dekoratorów
#     - Każdy zestaw danych jest testowany w obu implementacjach
#     - assert porównuje rzeczywisty wynik funkcji z oczekiwanym
#
# 6️⃣ Dzięki temu jednym testem sprawdzamy DWIE wersje funkcji
#     bez powielania tych samych danych testowych.
#
# ✅ Efekt w konsoli (pytest -v):
#     test_pytest_promo.py::test_is_valid_promo_functions[is_valid_promo-ABC123XY90] PASSED
#     test_pytest_promo.py::test_is_valid_promo_functions[is_valid_promo_and-ABC123XY90] PASSED
#     ...
# ==============================================================
