# Kalkulator OOP

## Opis projektu

Kalkulator obiektowy uruchamiany z linii poleceń.
Projekt demonstruje podstawy OOP w Pythonie — enkapsulację logiki w klasie,
obsługę błędów oraz pisanie testów jednostkowych.

## Technologie

- **Python 3** - język projektu
- **pytest** - testy automatyczne

## Struktura projektu

```
Kalkulator/
├── README.md
├── requirements.txt
├── .gitignore
├── calculate.py        # klasa Calculator: operacje matematyczne + historia
└── tests/
    ├── __init__.py
    └── test_calculate.py   # 8 testów jednostkowych
```

## Jak uruchomić

### 1. Utwórz i aktywuj środowisko wirtualne

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / Mac
source .venv/bin/activate
```

### 2. Zainstaluj zależności

```bash
pip install -r requirements.txt
```

### 3. Uruchom kalkulator

```bash
python calculate.py
```

## Testy

```bash
# Windows
.venv\Scripts\python.exe -m pytest tests/ -v

# Linux / Mac
pytest tests/ -v
```

## Przykład użycia

```
Prosty kalkulator.

Podaj operację (+, -, *, /, ^) lub 'exit' aby zakończyć: +
Podaj pierwszą liczbę: 10
Podaj drugą liczbę: 5
Wynik: 15.0

Podaj operację (+, -, *, /, ^) lub 'exit' aby zakończyć: exit

--- Historia operacji ---
10.0 + 5.0 = 15.0
-------------------------
```

## Obsługiwane operacje

| Symbol | Operacja      |
|--------|---------------|
| `+`    | Dodawanie     |
| `-`    | Odejmowanie   |
| `*`    | Mnożenie      |
| `/`    | Dzielenie     |
| `^`    | Potęgowanie   |

## Testy jednostkowe — pokryte scenariusze

| Test | Co sprawdza |
|------|-------------|
| `test_add` | dodawanie dwóch liczb |
| `test_subtract` | odejmowanie |
| `test_multiply` | mnożenie |
| `test_divide` | dzielenie |
| `test_divide_by_zero` | czy rzuca `ZeroDivisionError` |
| `test_power` | potęgowanie |
| `test_unknown_operation` | czy rzuca `ValueError` na nieznaną operację |
| `test_history` | czy wyniki zapisują się do historii |

## Kluczowe wzorce

### Mapowanie operacji przez słownik

Zamiast łańcucha `if/elif`, operacje są przechowywane jako funkcje w słowniku.
Dodanie nowej operacji wymaga jednej linii — bez modyfikacji logiki `calculate()`.

```python
operation_map = {
    "+": self.add,
    "-": self.subtract,
    ...
}
func = operation_map.get(operation)
```

### Separacja logiki od I/O

Klasa `Calculator` nie wie nic o terminalu — przyjmuje liczby, zwraca wyniki.
Cała interakcja z użytkownikiem jest w bloku `if __name__ == "__main__"`.
