# Obsluga wyjatkow

try / except / else / finally / raise - kompletne cwiczenia.

## Zawartosc

| Plik | Opis |
|------|------|
| `try_except_cwiczenia.py` | 10 cwiczen: dzielenie, walidacja input, JSON, parsowanie list, operacje na plikach |

## Wzorce

```python
try:
    # kod ktory moze rzucic wyjatek
except ValueError as e:
    # obsluga blednych danych
except FileNotFoundError:
    # brak pliku
else:
    # wykonuje sie gdy NIE bylo wyjatku
finally:
    # wykonuje sie ZAWSZE (sprzatanie)
```

## Powiazania

- Cwiczenia z plikami w `Pliki_i_JSON/cwiczenia/` lacza wyjatki z obsluga plikow
- Walidacja danych w `Funkcje/cwiczenia/`
