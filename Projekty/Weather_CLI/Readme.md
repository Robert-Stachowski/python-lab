# Weather CLI

## Opis projektu

Minimalistyczny klient API pogodowego uruchamiany z linii poleceń.
Projekt pokazuje jak budować testowalny CLI tool w Pythonie — z poprawną architekturą,
obsługą błędów i izolowanymi testami jednostkowymi bez dostępu do sieci.

## Technologie

- **Python 3** - język projektu
- **requests** - komunikacja HTTP, `requests.Session`
- **argparse** - interfejs linii poleceń
- **pytest** - testy automatyczne
- **unittest.mock** - mockowanie zależności w testach

## Struktura projektu

```
Weather_CLI/
├── Readme.md
├── requirements.txt
├── conftest.py              # sys.path fix dla pytest
├── .gitignore
├── main.py                  # warstwa CLI: build_parser(), main() -> int
├── weather_client.py        # WeatherClient: requester pattern, Session, walidacja
├── tests/
│   ├── __init__.py
│   ├── test_weather_client.py   # 6 testów klienta HTTP
│   └── test_main.py             # 4 testy CLI
└── docs/
    ├── NOTATKI.md               # notatki edukacyjne
    ├── WEATHER_CLIENT.md        # omówienie weather_client.py linijka po linijce
    ├── MAIN.md                  # omówienie main.py linijka po linijce
    └── TESTY.md                 # omówienie testów linijka po linijce
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

### 3. Uruchom program

```bash
python main.py Warszawa
```

## Testy

```bash
# Windows
.venv\Scripts\python.exe -m pytest tests/ -v

# Linux / Mac
pytest tests/ -v
```

Testy są szybkie, deterministyczne i nie korzystają z internetu — wszystkie żądania HTTP są mockowane.

## Przykład użycia

```bash
$ python main.py Poznań
Pobieram dane pogodowe dla miasta: Poznań
Miasto:      Poznań
Temperatura: 10.0°C
Pogoda:      clouds
```

## Scenariusze błędów

| Sytuacja | Exit code |
|----------|-----------|
| Sukces | 0 |
| Błędne dane wejściowe, brak pól w JSON | 1 |
| Błąd sieci, błąd HTTP, nieoczekiwany błąd | 2 |

## Kluczowe wzorce

### Requester pattern

`WeatherClient` przyjmuje opcjonalny argument `requester` — w produkcji używa prawdziwego `requests`,
w testach dostaje `Mock()`. Umożliwia pełne mockowanie bez sieci.

```python
client = WeatherClient()              # produkcja — prawdziwy requests
client = WeatherClient(requester=Mock())  # test — mock
```

### Walidacja JSON przez zbiory

```python
required = {"city", "temp_c", "condition"}
if not required <= data.keys():
    raise ValueError("Brak wymaganych pól")
```

### Separation of concerns

- `weather_client.py` — logika HTTP: sesja, walidacja, parsowanie JSON
- `main.py` — warstwa CLI: argumenty, obsługa błędów, exit codes

## Testy jednostkowe — pokryte scenariusze

| Test | Co sprawdza |
|------|-------------|
| `test_get_city_weather_happy_path` | poprawny przepływ + asercja na wywołanie HTTP |
| `test_get_city_weather_http_error` | serwer zwrócił 4xx/5xx |
| `test_get_city_weather_connection_error` | brak sieci / timeout |
| `test_invalid_values_get_city_weather` | walidacja wejścia (4 wartości, parametrize) |
| `test_get_city_weather_missing_fields` | JSON bez wymaganych pól |
| `test_get_weather_city_invalid_json` | odpowiedź serwera nie jest JSON-em |
| `test_build_parser` | parser mapuje argument na atrybut `city_name` |
| `test_main_happy_path` | pełny przepływ main() + weryfikacja stdout |
| `test_main_value_error` | ValueError → exit code 1 |
| `test_main_generic_exception` | Exception → exit code 2 |

## Materiały edukacyjne

Katalog `docs/` zawiera omówienie każdego pliku projektu linijka po linijce:

| Plik | Temat |
|------|-------|
| `WEATHER_CLIENT.md` | WeatherClient — dependency injection, Session, walidacja |
| `MAIN.md` | main.py — argparse, exit codes, separation of concerns |
| `TESTY.md` | testy — Mock, patch, parametrize, capsys, side_effect |
| `NOTATKI.md` | skrócone notatki z kluczowymi wzorcami |
