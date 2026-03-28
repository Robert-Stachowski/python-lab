# Mini Explorer CLI

Narzędzie do eksploracji systemu plików z poziomu terminala.

## Funkcje

- Listowanie zawartości katalogu
- Liczenie plików w katalogu
- Filtrowanie plików po rozszerzeniu
- Wyświetlanie informacji o pliku (nazwa, rozszerzenie, rozmiar, typ)

## Technologie

- Python 3.4+
- `argparse` — parsowanie argumentów CLI
- `pathlib` — operacje na ścieżkach (nowoczesne podejście zamiast `os.path`)
- `pytest` — testy jednostkowe

## Instalacja

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Użycie

```bash
python mini_explorer_cli.py <ścieżka> [flaga]
```

| Flaga | Skrót | Opis |
|-------|-------|------|
| `--count` | `-c` | wypisz liczbę plików w katalogu |
| `--list` | `-l` | wypisz zawartość katalogu |
| `--ext <rozszerzenie>` | `-e` | filtruj pliki po rozszerzeniu |
| `--info` | `-i` | wyświetl informacje o pliku |

### Przykłady

```bash
# katalog
python mini_explorer_cli.py .
python mini_explorer_cli.py . --count
python mini_explorer_cli.py . --list
python mini_explorer_cli.py . --ext .py

# plik
python mini_explorer_cli.py mini_explorer_cli.py --info
```

## Kody wyjścia

| Kod | Znaczenie |
|-----|-----------|
| `0` | operacja wykonana poprawnie |
| `1` | błąd (ścieżka nie istnieje, nieoczekiwany wyjątek) |
| `2` | złe użycie (zła kombinacja flag, brak flagi) |

## Uruchamianie testów

```bash
pytest tests/ -v
```

## Struktura projektu

```
Mini_Explorer_CLI/
├── mini_explorer_cli.py
├── requirements.txt
├── tests/
│   ├── __init__.py
│   └── test_mini_explorer_cli.py
└── docs/
    ├── Notes_Mini_Explorer_CLI.md
    └── Notes_Testy.md
```
