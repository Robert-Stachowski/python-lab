# Notatki do projektu Weather CLI

Notatki edukacyjne wydzielone z kodu źródłowego.
Nie są częścią produkcyjnego kodu — służą jako materiał do nauki i powtórki.

---

## main.py

### build_parser()

Funkcja buduje parser argumentów linii poleceń i przyjmuje jeden argument pozycyjny — `city_name`.

argparse konwertuje wpisaną wartość na atrybut `args.city_name`, dostępny po wywołaniu `parser.parse_args()`.

Wydzielona osobno, żeby dało się ją testować niezależnie i żeby `main()` było czyste.

---

### Obsługa wyjątków i semantyka exit code

```
except ValueError  → return 1   # błąd użytkownika (złe dane, brak pól w JSON)
except Exception   → return 2   # błąd systemowy (sieć, API, nieoczekiwany błąd)
brak wyjątku       → return 0   # sukces
```

Exit codes `0/1/2` to standard UNIX-owy. Skrypt używany w automatyzacji lub CI/CD
może sprawdzić kod wyjścia i zareagować inaczej na błąd użytkownika vs awarię systemu.

---

### `raise SystemExit(main())`

`main()` zwraca `int` (exit code). `SystemExit` przekazuje tę liczbę do systemu operacyjnego.

Dzięki temu plik można importować w testach (`if __name__ == "__main__"` nie uruchamia się przy imporcie)
i wywoływać `main()` bezpośrednio — bez uruchamiania całego procesu.

---

## weather_client.py

### Walidacja wejścia

```python
if city is None or not isinstance(city, str) or not city.strip():
    raise ValueError(...)
```

Sprawdzamy kolejno: `None`, nie-string (np. liczba), pusty string lub sam whitespace.
Kolejność ma znaczenie — gdybyśmy wywołali `.strip()` na `None`, dostalibyśmy `AttributeError` zamiast `ValueError`.

---

### Walidacja pól JSON

```python
required = {"temp_c", "condition"}
if not required <= data.keys():
    raise ValueError("Brak wymaganych pól")
```

Operator `<=` na zbiorach oznacza "czy jest podzbiorem".
`required <= data.keys()` zwraca `True` gdy KAŻDY klucz z `required` istnieje w `data`.
To samo co `"temp_c" in data and "condition" in data`, ale łatwiej rozszerzalne —
żeby dodać nowe wymagane pole wystarczy dopisać je do zbioru `required`.

---

## tests/test_weather_client.py

### Fixture `client_and_session`

```python
fake_requester = Mock()
fake_session = Mock()
fake_requester.Session.return_value = fake_session
client = WeatherClient(requester=fake_requester)
```

`WeatherClient.__init__` wywołuje `self.requester.Session()` — dlatego mockujemy `fake_requester.Session.return_value`,
żeby zamiast prawdziwej sesji HTTP dostać `fake_session`, którą możemy kontrolować w testach.

Fixture zwraca krotkę `(client, fake_session)`. W każdym teście rozpakowujemy:
```python
client, fake_session = client_and_session
```

---

### Happy path — co sprawdzamy

```python
fake_session.get.assert_called_once_with(expected_url, timeout=5)
```

Asercja na `assert_called_once_with` sprawdza **czy** metoda została wywołana i **z jakimi argumentami**.
Gdyby klient zmienił URL albo timeout — test by upadł. To celowe — test "pilnuje kontraktu" wywołania HTTP.

---

### `side_effect` vs `return_value`

- `return_value` — gdy metoda jest wywołana, zwróć tę wartość
- `side_effect` — gdy metoda jest wywołana, rzuć ten wyjątek (lub wywołaj tę funkcję)

Używamy `side_effect` gdy chcemy zasymulować wyjątek:
```python
fake_response.raise_for_status.side_effect = HTTPError("404")
fake_session.get.side_effect = ConnectionError("network down")
fake_response.json.side_effect = ValueError("invalid JSON")
```

---

### `raise_for_status.return_value = None`

`raise_for_status()` w `requests` nic nie zwraca gdy status jest OK — po prostu nie rzuca wyjątku.
`return_value = None` symuluje właśnie tę sytuację (odpowiednik HTTP 200).

Nie trzeba tego ustawiać na Mocku (Mock domyślnie zwraca Mock gdy nie ustawiono return_value),
ale jawne `= None` czyni intencję czytelną: "symulujemy brak błędu".

---

### `fake_response.json.return_value = {}` w teście HTTP error

W teście `test_get_city_weather_http_error` ustawiamy `json.return_value = {}` mimo że `json()` nie zostanie wywołane
(kod wywala się wcześniej na `raise_for_status()`).

Ta linijka jest **zbędna** — Mock automatycznie tworzy atrybuty przy pierwszym dostępie,
więc `json()` nigdy nie rzuciłoby `AttributeError`. To pozostałość po nadmiarowym komentarzu.
Można ją usunąć bez żadnego wpływu na wynik testu.

---

### `@pytest.mark.parametrize`

```python
INVALID_VALUES = ["", " ", None, 123]

@pytest.mark.parametrize("city", INVALID_VALUES)
def test_invalid_values_get_city_weather(client_and_session, city):
```

`parametrize` uruchamia ten sam test wielokrotnie z różnymi wartościami.
Zamiast pisać 4 osobne testy — piszemy jeden. pytest generuje osobny wynik dla każdej wartości.

`_` w `client, _ = client_and_session` — konwencja "ta wartość mnie nie interesuje" (sesja nie jest potrzebna przy walidacji wejścia, bo kod wywala się zanim dojdzie do wywołania HTTP).

---

## tests/test_main.py

### `patch("main.WeatherClient")` — dlaczego nie `patch("weather_client.WeatherClient")`?

Kiedy `main.py` wykonuje:
```python
from weather_client import WeatherClient
```

Python tworzy w przestrzeni nazw modułu `main` zmienną `WeatherClient` wskazującą na klasę.
To jest **kopia referencji**, niezależna od oryginału w `weather_client`.

Podmiana oryginału (`patch("weather_client.WeatherClient")`) nie zmieni kopii w `main`.
Trzeba podmienić referencję tam gdzie jest **używana** — czyli `patch("main.WeatherClient")`.

---

### `FakeClient.return_value`

`main()` robi `client = WeatherClient()` — wywołuje klasę jak konstruktor.
`FakeClient` to mock klasy, więc `FakeClient()` zwraca `FakeClient.return_value`.
To właśnie ten obiekt będzie "instancją" którą `main()` wywołuje dalej.

```python
FakeClient.return_value.get_city_weather.return_value = {...}
```

---

### `patch.object(sys, "argv", [...])`

`argparse` czyta argumenty z `sys.argv`. Normalnie `sys.argv[0]` to nazwa skryptu,
`sys.argv[1]` to pierwszy argument użytkownika.

```python
with patch.object(sys, "argv", ["prog", "Poznań"]):
```

Symulujemy wywołanie `python main.py Poznań` bez dotykania terminala.

---

### `capsys`

Wbudowany fixture pytest do przechwycenia tego co trafia na stdout/stderr.

```python
out = capsys.readouterr().out
assert "Pobieram dane pogodowe dla miasta: Poznań" in out
```

`readouterr()` zwraca namedtuple `(out, err)`. Wywołanie resetuje bufor — kolejne `readouterr()` nie zwróci tego co już odczytano.
