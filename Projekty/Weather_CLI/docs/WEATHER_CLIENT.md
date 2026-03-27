# Omówienie: weather_client.py

Plik linijka po linijce — co robi, po co, dlaczego tak a nie inaczej.

---

## Import

```python
import requests
```

Biblioteka do wysyłania zapytań HTTP. Używamy jej do komunikacji z API pogodowym.

---

## Klasa i `__init__`

```python
class WeatherClient:

    def __init__(self, requester=None):
```

### Dlaczego `requester=None` zamiast po prostu `def __init__(self)`?

Bo chcemy móc **testować klasę bez prawdziwego internetu**.

Gdyby klasa sama tworzyła sobie `requests.Session()` i nie dawała możliwości podstawienia czegoś innego,
w testach nie byłoby jak podmienić `requests` na `Mock()`.

`requester=None` to **otwarte drzwi** — możesz wsadzić tam cokolwiek z zewnątrz.
W testach wsadzasz `Mock()`, w produkcji nie podajesz nic i klasa sama używa prawdziwego `requests`.

To wzorzec zwany **dependency injection** — zamiast klasa sama tworzy swoje zależności, dostaje je z zewnątrz.

---

```python
self.base_url = "https://example_url.com/api"
```

Bazowy adres API. Przechowywany jako atrybut żeby nie powtarzać go w każdej metodzie.

---

```python
self.headers = {"Accept": "application/json"}
```

Nagłówek HTTP mówiący serwerowi: "oczekuję odpowiedzi w formacie JSON".

`requests` domyślnie ustawia `Accept: */*` (akceptuję wszystko). Jawne `application/json`
to standard przy pracy z REST API — serwer wie w jakim formacie ma odpowiedzieć.

---

```python
self.requester = requester or requests
```

Jeśli `requester=None` (nic nie podano) — użyj prawdziwego `requests`.
Jeśli podano `Mock()` — użyj tego.

`None or requests` zwraca `requests` bo `None` jest falsy.
`Mock() or requests` zwraca `Mock()` bo Mock nie jest falsy.

---

```python
self.session = self.requester.Session()
```

### Co to jest sesja?

Wyobraź sobie że dzwonisz na infolinię.

**Bez sesji** — każde zapytanie to nowe połączenie. Dzwonisz, przedstawiasz się, pytasz, rozłączasz.
Przy następnym pytaniu zaczynasz od nowa.

**Z sesją** — dzwonisz raz, przedstawiasz się i rozmawiasz dalej. Połączenie zostaje otwarte.

Technicznie `requests.Session()`:
- utrzymuje połączenie TCP — nie nawiązuje go od nowa przy każdym żądaniu (szybciej)
- zapamiętuje nagłówki — ustawiasz raz, wysyłane przy każdym żądaniu
- zapamiętuje cookies — jeśli serwer je ustawił, sesja je przechowuje automatycznie

---

```python
self.session.headers.update(self.headers)
```

"Wgrywa" nagłówki do sesji. Od teraz każde zapytanie wysyłane przez tę sesję
automatycznie zawiera `Accept: application/json` — bez powtarzania tego przy każdym `.get()`.

### Kolejność `__init__` w całości:
1. ustaw bazowy URL
2. ustaw nagłówki
3. wybierz bibliotekę (prawdziwa lub mock)
4. stwórz sesję
5. wgraj nagłówki do sesji

---

## Metoda `get_city_weather`

```python
def get_city_weather(self, city: str) -> dict:
```

Przyjmuje nazwę miasta jako string, zwraca słownik z danymi pogodowymi.

---

### Walidacja wejścia

```python
if city is None or not isinstance(city, str) or not city.strip():
    raise ValueError("Brak danych / Niepoprawne dane")
```

Trzy warunki, kolejność ma znaczenie:

1. `city is None` — czy w ogóle coś podano
2. `not isinstance(city, str)` — czy to string (nie liczba, lista itp.)
3. `not city.strip()` — czy to nie jest sama spacja (`" ".strip()` → `""` → falsy)

**Dlaczego ta kolejność?**

`city.strip()` wymaga że `city` jest stringiem — `None.strip()` rzuciłoby `AttributeError`.
Dzięki `or` Python sprawdza warunki od lewej i zatrzymuje się przy pierwszym `True` (**short-circuit evaluation**).
Gdy `city is None` — pozostałe warunki w ogóle nie są sprawdzane.

---

### Budowanie URL i zapytanie HTTP

```python
url = f"{self.base_url}/weather"
response = self.session.get(url, params={"city": city}, timeout=5)
```

**Dlaczego `params=` zamiast sklejania stringa?**

Dwie zalety:
1. Czytelność — URL i parametry rozdzielone, widać co jest czym
2. Enkodowanie — `requests` sam zamienia spacje i znaki specjalne.
   "New York" staje się `?city=New+York` automatycznie.
   Przy ręcznym sklejaniu musiałbyś to obsługiwać sam.

**`timeout=5`** — czas oczekiwania w sekundach, nie liczba prób.
Jeśli serwer nie odpowie w ciągu 5 sekund, `requests` przerywa i rzuca `ConnectionError`.
Bez tego program czekałby w nieskończoność.

---

### Sprawdzenie kodu HTTP

```python
response.raise_for_status()
```

Serwer w odpowiedzi zawsze zwraca kod statusu — 200 (OK), 404 (nie znaleziono), 500 (błąd serwera).

`raise_for_status()` sprawdza ten kod i jeśli jest błędowy (4xx lub 5xx) — rzuca `HTTPError`.
Jeśli 200 — nie robi nic.

Bez tego musiałbyś pisać ręcznie:
```python
if response.status_code != 200:
    raise HTTPError(...)
```

---

### Parsowanie odpowiedzi

```python
data = response.json()
```

Parsuje odpowiedź z serwera (surowy tekst JSON) na słownik Pythona.
Po tej linijce `data` to normalny dict — można robić `data["city"]` itd.

---

### Walidacja pól

```python
required = {"city", "temp_c", "condition"}

if not required <= data.keys():
    raise ValueError("Brak wymaganych pól")
```

`<=` między zbiorami oznacza **"czy jestem podzbiorem"** — czy wszystkie elementy z lewej są w prawej.

```python
{"city", "temp_c"} <= {"city", "temp_c", "condition"}  # True
{"city", "wind"}   <= {"city", "temp_c", "condition"}  # False — brak "wind"
```

Jeśli API zwróci JSON bez wymaganych kluczy — rzucamy `ValueError` zanim dane trafią dalej.

Zaleta zbioru vs ręczne sprawdzanie:
```python
# zamiast tego:
if "city" not in data or "temp_c" not in data or "condition" not in data:
# wystarczy dodać klucz do zbioru required
```

---

### Zwrot danych

```python
return data
```

Zwraca słownik z danymi pogodowymi. `main.py` odbiera go i wyświetla użytkownikowi.

---

## Przepływ end-to-end

```
wywołanie get_city_weather("Warszawa")
    ↓
walidacja wejścia (None / typ / whitespace)
    ↓
zbuduj URL + wyślij GET z params= i timeout=
    ↓
sprawdź kod HTTP (raise_for_status)
    ↓
sparsuj JSON na dict
    ↓
sprawdź czy dict ma wymagane pola
    ↓
zwróć dict → main.py wyświetla wynik
```
