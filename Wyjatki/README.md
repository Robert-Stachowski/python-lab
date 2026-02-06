# Obsługa wyjątków

try / except / else / finally / raise - kompletne cwiczenia.

## Zawartość

| Plik | Opis |
|------|------|
| `try_except_cwiczenia.py` | 10 cwiczen: dzielenie, walidacja input, JSON, parsowanie list, operacje na plikach |

## Wzorce

```python
try:
    # kod który może rzucic wyjątek
except ValueError as e:
    # obsługa błędnych danych
except FileNotFoundError:
    # brak pliku
else:
    # wykonuje się gdy NIE było wyjątku
finally:
    # wykonuje się ZAWSZE (sprzątanie)
```

## Powiązania

- Ćwiczenia z plikami w `Pliki_i_JSON/cwiczenia/` łączą wyjatki z obsługą plikow
- Walidacja danych w `Funkcje/cwiczenia/`
