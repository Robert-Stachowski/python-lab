# Omówienie: tests/

Pliki testów linijka po linijce — co robi, po co, dlaczego tak a nie inaczej.

---

## test_weather_client.py

### Importy

```python
import pytest
from requests.exceptions import HTTPError, ConnectionError
from unittest.mock import Mock
from weather_client import WeatherClient
```

`Mock` — fałszywy obiekt który udaje prawdziwy. Możesz mu ustawić co zwraca i sprawdzić czy był wywołany.

`HTTPError`, `ConnectionError` — importujemy z `requests.exceptions` bo tych wyjątków używamy w testach do symulowania błędów.

---

### Fixture `client_and_session`

```python
@pytest.fixture
def client_and_session():
    fake_requester = Mock()
    fake_session = Mock()
    fake_requester.Session.return_value = fake_session
    client = WeatherClient(requester=fake_requester)
    return client, fake_session
```

**Po co dwa Mocki, a nie jeden?**

Bo `WeatherClient.__init__` robi dwa kroki:
1. `self.requester.Session()` — wywołuje `.Session()` na bibliotece
2. `self.session.get(...)` — wywołuje `.get()` na sesji

To są dwa różne obiekty. `fake_requester` to mock biblioteki `requests`, `fake_session` to mock sesji którą ta biblioteka zwraca.

Linijka `fake_requester.Session.return_value = fake_session` łączy je razem — mówi Mockowi: "gdy ktoś wywoła `.Session()` na `fake_requester`, zwróć `fake_session`".

**Dlaczego fixture zwraca oba?**

W testach potrzebujemy:
- `client` — żeby wywołać metodę którą testujemy
- `fake_session` — żeby sprawdzić czy `.get()` zostało wywołane z właściwymi argumentami

**Rozpakowywanie w teście:**

```python
client, fake_session = client_and_session
```

Fixture zwraca krotkę `(client, fake_session)` — rozpakowujesz ją na dwie zmienne w jednej linijce.

---

### `test_get_city_weather_happy_path`

```python
def test_get_city_weather_happy_path(client_and_session):
    client, fake_session = client_and_session

    fake_response = Mock()
    fake_response.raise_for_status.return_value = None
    fake_response.json.return_value = {
        "city": "Poznań",
        "temp_c": 10.0,
        "condition": "clouds"
    }
    fake_session.get.return_value = fake_response

    result = client.get_city_weather("Poznań")

    assert result == {"city": "Poznań", "temp_c": 10.0, "condition": "clouds"}
    fake_session.get.assert_called_once_with(
        "https://example_url.com/api/weather",
        params={"city": "Poznań"},
        timeout=5
    )
```

**Po co trzeci Mock — `fake_response`?**

`session.get()` zwraca obiekt response, na którym wywołujesz dwie metody:
- `.raise_for_status()` — sprawdzenie kodu HTTP
- `.json()` — parsowanie odpowiedzi

Gdybyś ustawił `fake_session.get.return_value = {"city": ...}` — dostałbyś surowy słownik.
Na słowniku nie możesz wywołać `.raise_for_status()` ani `.json()` — `KeyError` lub `AttributeError`.

`fake_response = Mock()` daje obiekt z obu tych metod.

**`raise_for_status.return_value = None`**

`raise_for_status()` w `requests` nic nie zwraca gdy status jest OK — po prostu nie rzuca wyjątku.
`return_value = None` symuluje tę sytuację (odpowiednik HTTP 200). Jawne `= None` czyni intencję czytelną: "symulujemy brak błędu".

**Dwie asercje:**

```python
assert result == {...}
```
Sprawdza czy zwrócone dane są poprawne.

```python
fake_session.get.assert_called_once_with(...)
```
Sprawdza **czy** `.get()` zostało wywołane, **ile razy** (raz) i **z jakimi argumentami**.
Bez tej asercji test nie wykryłby błędnego URL ani pominiętego `timeout`.

---

### `test_get_city_weather_http_error`

```python
def test_get_city_weather_http_error(client_and_session):
    client, fake_session = client_and_session

    fake_response = Mock()
    fake_response.raise_for_status.side_effect = HTTPError("404")
    fake_session.get.return_value = fake_response

    with pytest.raises(HTTPError):
        client.get_city_weather("fake_city")
```

**`side_effect` vs `return_value`**

- `return_value` — gdy metoda jest wywołana, **zwróć tę wartość**
- `side_effect` — gdy metoda jest wywołana, **rzuć ten wyjątek**

Używamy `side_effect` gdy chcemy zasymulować błąd.

**Częsta pułapka:**

```python
# ŹLE — zwraca obiekt wyjątku jako wartość, nikt go nie rzuca
fake_response.raise_for_status.return_value = HTTPError("404")

# DOBRZE — Mock rzuca wyjątek gdy metoda jest wywołana
fake_response.raise_for_status.side_effect = HTTPError("404")
```

Przy `return_value = HTTPError("404")` kod szedłby dalej jakby nic się nie stało —
obiekt wyjątku zostałby po cichu zignorowany. Test by nie wykrył błędu.

**`pytest.raises(HTTPError)`**

Context manager który sprawdza czy wewnątrz bloku został rzucony oczekiwany wyjątek.
Jeśli wyjątek nie zostanie rzucony — test pada.

---

### `test_get_city_weather_connection_error`

```python
def test_get_city_weather_connection_error(client_and_session):
    client, fake_session = client_and_session

    fake_session.get.side_effect = ConnectionError("network down")

    with pytest.raises(ConnectionError):
        client.get_city_weather("fake_city")
```

Tu `side_effect` jest na `fake_session.get` — czyli błąd rzucany jest **przy samym wysyłaniu zapytania**, zanim w ogóle dostaniesz response.

**Różnica między HTTP error a Connection error — moment błędu:**

```python
response = self.session.get(url, ...)   # ConnectionError rzuca się TUTAJ
response.raise_for_status()             # HTTPError rzuca się TUTAJ
```

- `ConnectionError` — `.get()` nie doszło do serwera (brak sieci, timeout, serwer niedostępny).
  Response nigdy nie powstaje — dlatego w teście nie ma `fake_response` w ogóle.
- `HTTPError` — zapytanie dotarło, serwer odpowiedział błędem (404, 500).
  Masz response, ale `raise_for_status()` go odrzuca.

---

### `@pytest.mark.parametrize`

```python
INVALID_VALUES = ["", " ", None, 123]

@pytest.mark.parametrize("city", INVALID_VALUES)
def test_invalid_values_get_city_weather(client_and_session, city):
    client, _ = client_and_session

    with pytest.raises(ValueError):
        client.get_city_weather(city)
```

**Po co `parametrize`?**

Zamiast pisać 4 osobne testy (jeden dla `""`, jeden dla `" "`, jeden dla `None`, jeden dla `123`) — piszesz jeden. pytest uruchamia go 4 razy z różnymi wartościami i pokazuje osobny wynik dla każdej.

```
PASSED test_invalid_values_get_city_weather[""]
PASSED test_invalid_values_get_city_weather[" "]
PASSED test_invalid_values_get_city_weather[None]
PASSED test_invalid_values_get_city_weather[123]
```

**`_` zamiast `fake_session`**

```python
client, _ = client_and_session
```

Konwencja Pythona — `_` oznacza "ta wartość mnie nie interesuje". Sesja nie jest potrzebna bo kod wywala się na walidacji wejścia, zanim dojdzie do wywołania HTTP.

---

### `test_get_city_weather_missing_fields`

```python
def test_get_city_weather_missing_fields(client_and_session):
    client, fake_session = client_and_session

    fake_response = Mock()
    fake_response.raise_for_status.return_value = None
    fake_response.json.return_value = {"city": "Poznań"}  # brak temp_c i condition

    fake_session.get.return_value = fake_response

    with pytest.raises(ValueError):
        client.get_city_weather("Poznań")
```

Testuje walidację `required <= data.keys()`. API zwróciło JSON, ale bez wymaganych pól — klient powinien rzucić `ValueError`.

Kod wywala się tutaj:
```python
data = response.json()            # działa — zwraca {"city": "Poznań"}
if not required <= data.keys():   # wywala się — brakuje temp_c i condition
    raise ValueError(...)
```

---

### `test_get_weather_city_invalid_json`

```python
def test_get_weather_city_invalid_json(client_and_session):
    client, fake_session = client_and_session

    fake_response = Mock()
    fake_response.raise_for_status.return_value = None
    fake_response.json.side_effect = ValueError("invalid JSON")

    fake_session.get.return_value = fake_response

    with pytest.raises(ValueError):
        client.get_city_weather("poznań")
```

`response.json()` rzuca `ValueError` gdy odpowiedź serwera nie jest poprawnym JSON-em
(np. serwer zwrócił HTML zamiast JSON, albo odpowiedź jest uszkodzona).

Kod wywala się tutaj:
```python
data = response.json()            # wywala się — nie ma czego parsować
if not required <= data.keys():   # nigdy nie dochodzi
```

**Różnica między `missing_fields` a `invalid_json`:**

| | `missing_fields` | `invalid_json` |
|---|---|---|
| `response.json()` | działa, zwraca dict | rzuca `ValueError` |
| walidacja pól | wywala się | nigdy nie dochodzi |
| przyczyna | niekompletna odpowiedź API | odpowiedź nie jest JSON-em |

---

## test_main.py

### `Mock` vs `patch` — kiedy którego używać

- `Mock()` — tworzysz fałszywy obiekt i **sam go przekazujesz** do testowanego kodu (przez argument, fixture)
- `patch` — **podmieniasz** obiekt w module na fałszywy, bez ruszania kodu który go używa

W `test_weather_client.py` używałeś `Mock()` bo `WeatherClient` przyjmuje `requester` jako argument — miałeś otwarte drzwi do wstrzyknięcia mocka.

W `test_main.py` nie ma żadnych drzwi:
```python
client = WeatherClient()  # tworzy sobie sam, nic nie przyjmuje z zewnątrz
```
Musisz podmienić `WeatherClient` w module `main` zanim kod go użyje — do tego służy `patch`.

---

### `test_build_parser`

```python
def test_build_parser():
    parser = build_parser()
    args = parser.parse_args(["Warszawa"])
    assert args.city_name == "Warszawa"
```

**Dlaczego `parse_args(["Warszawa"])` przyjmuje listę a nie stringa?**

Bo `sys.argv` — skąd normalnie `argparse` czyta argumenty — jest listą:
```python
# gdy użytkownik wpisuje: python main.py Warszawa
sys.argv == ["main.py", "Warszawa"]
```
Gdybyś przekazał sam string `"Warszawa"` — `argparse` rozbiłby go na litery: `["W", "a", "r", "s", ...]`.

**Skąd `args.city_name` — dlaczego nie `args.city` ani `args.name`?**

Nazwa atrybutu pochodzi z `add_argument` w `build_parser()`:
```python
parser.add_argument("city_name", ...)  # ← ta nazwa staje się args.city_name
```

---

### `test_main_happy_path`

```python
def test_main_happy_path(capsys):
    with patch("main.WeatherClient") as FakeClient:
        fake_client_instance = FakeClient.return_value
        fake_client_instance.get_city_weather.return_value = {
            "city": "Poznań",
            "temp_c": 10.0,
            "condition": "clouds"
        }

        with patch.object(sys, "argv", ["prog", "Poznań"]):
            exit_code = main()

    assert exit_code == 0
    out = capsys.readouterr().out
    assert "Pobieram dane pogodowe dla miasta: Poznań" in out
    assert "Miasto:" in out
    assert "Temperatura:" in out
```

**`patch("main.WeatherClient")` — dlaczego nie `patch("weather_client.WeatherClient")`?**

Gdy `main.py` robi `from weather_client import WeatherClient`, Python tworzy w przestrzeni nazw
modułu `main` zmienną `WeatherClient` — **kopię referencji**, niezależną od oryginału.

Podmiana oryginału w `weather_client` nie zmieni kopii w `main`.
Trzeba podmienić referencję tam gdzie jest **używana** — czyli `patch("main.WeatherClient")`.

**`FakeClient.return_value`**

`main()` robi `client = WeatherClient()` — wywołuje klasę jak konstruktor.
`FakeClient` to mock klasy, więc `FakeClient()` zwraca `FakeClient.return_value`.
To właśnie ten obiekt będzie "instancją" używaną dalej w `main()`.

**`patch.object(sys, "argv", ["prog", "Poznań"])`**

`argparse` czyta argumenty z `sys.argv`. Normalnie `sys.argv[0]` to nazwa skryptu,
`sys.argv[1]` to pierwszy argument użytkownika.

Symulujemy wywołanie `python main.py Poznań` bez dotykania terminala.

**`capsys`**

Wbudowany fixture pytest do przechwycenia tego co program wypisuje przez `print()`.
Bez niego nie mógłbyś sprawdzić co `main()` wypisało na ekran.

```python
out = capsys.readouterr().out
assert "Miasto:" in out
```

`readouterr()` zwraca namedtuple `(out, err)`. Wywołanie resetuje bufor —
kolejne `readouterr()` nie zwróci tego co już odczytano.

**Dlaczego asercje używają `in` a nie `==`?**

```python
assert "Temperatura: 10.0°C" == out  # kruche — zmiana formatu psuje test
assert "Temperatura:" in out          # odporne — sprawdza czy w ogóle jest
```

`in` sprawdza czy fragment jest zawarty w stringu — nie musisz znać dokładnej wartości
żeby sprawdzić czy program w ogóle ją wypisał.

---

### `test_main_value_error` i `test_main_generic_exception`

```python
# test_main_value_error
fake_client_instance.get_city_weather.side_effect = ValueError("Brak danych")
# ...
assert exit_code == 1
assert "błąd: Brak danych" in out

# test_main_generic_exception
fake_client_instance.get_city_weather.side_effect = Exception("boom")
# ...
assert exit_code == 2
assert "błąd krytyczny:" in out
```

Testujemy dwie gałęzie obsługi błędów z `main()`. Każdy test sprawdza:
- czy exit code jest właściwy (1 lub 2)
- czy właściwy komunikat trafił na stdout

**Dlaczego `side_effect` a nie `return_value`?**

Chcemy żeby `get_city_weather()` **rzuciło** wyjątek — nie zwróciło go jako wartość.
`return_value = ValueError(...)` zwróciłby obiekt wyjątku jako `data`, a `main()` próbowałby
zrobić `data["city"]` — `KeyError`. `side_effect` powoduje że wyjątek jest rzucony i `except` go łapie.

**Dlaczego dwa osobne testy a nie jeden?**

`ValueError` i `Exception` to dwie różne gałęzie `except` w `main()`:
- `ValueError` → przewidziany błąd (zły input, brak pól) → exit code `1`
- `Exception` → wszystko inne (awaria sieci, nieoczekiwany błąd) → exit code `2`

Jeden test nie sprawdziłby obu gałęzi — każda wymaga osobnego testu.

---

## Wzorzec AAA

Każdy test w projekcie stosuje wzorzec **Arrange → Act → Assert**:

```
Arrange  — przygotuj dane i mocki (fake_response, return_value, side_effect)
Act      — wywołaj testowaną metodę (client.get_city_weather / main())
Assert   — sprawdź wynik (assert result == ... / assert exit_code == ...)
```

---

## Mapa testów — co każdy sprawdza

| Test | Co testuje |
|------|-----------|
| `test_get_city_weather_happy_path` | poprawny przepływ + asercja na wywołanie HTTP |
| `test_get_city_weather_http_error` | serwer zwrócił 4xx/5xx |
| `test_get_city_weather_connection_error` | brak sieci / timeout |
| `test_invalid_values_get_city_weather` | walidacja wejścia (4 wartości) |
| `test_get_city_weather_missing_fields` | JSON bez wymaganych pól |
| `test_get_weather_city_invalid_json` | odpowiedź serwera nie jest JSON-em |
| `test_build_parser` | parser mapuje argument na atrybut |
| `test_main_happy_path` | pełny przepływ main() + stdout |
| `test_main_value_error` | ValueError → exit code 1 |
| `test_main_generic_exception` | Exception → exit code 2 |
