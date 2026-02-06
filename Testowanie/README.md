# Testowanie w Pythonie

unittest i pytest - ściągi, ćwiczenia, przykłady z mock i fixtures.

## Zawartość

| Plik | Opis |
|------|------|
| `unittest_sciaga.py` | Kompletna ściąga unittest: assertions, setUp/tearDown, mock, subTest |

### cwiczenia/

| Plik | Opis |
|------|------|
| `unittest_cwiczenia.py` | 20+ ćwiczeń unittest: assertEqual, assertRaises, mock, subTest |
| `unittest_cwiczenia_02.py` | 10 zaawansowanych: assertAlmostEqual, tempfile, sys.argv, @patch |

### pytest_przyklady/

Kompletne przykłady pytest z kodem źródłowym i testami:

| Kod | Test | Co testuje |
|-----|------|------------|
| `pytest01.py` | `test_pytest01.py` | Prosta funkcja add() |
| `pytest_promo.py` | `test_pytest_promo.py` | Walidacja kodu promo z @parametrize |
| `bank_account.py` | `test_bank_account.py` | Klasa BankAccount - 13+ testow |

## Kluczowe pojęcia

- `assertEqual`, `assertTrue`, `assertRaises` - podstawowe asercje
- `setUp` / `tearDown` - przygotowanie i sprzątanie
- `@patch` / `mock` - mockowanie zależności
- `@pytest.mark.parametrize` - testy z wieloma danymi
- `fixtures` - przygotowanie danych testowych w pytest
