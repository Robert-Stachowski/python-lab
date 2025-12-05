# 🌦️ Weather CLI – Profesjonalny, Testowalny Klient API w Pythonie

Weather CLI to minimalistyczny, lecz w pełni profesjonalny projekt pokazujący,
jak tworzyć testowalne narzędzia linii poleceń (CLI) wykorzystujące:

- argparse (interfejs CLI),
- requests.Session (komunikacja z API),
- requester pattern (mockowalność),
- pełną obsługę błędów,
- semantykę exit code zgodną z UNIX,
- pytest + unittest.mock (testy klienta i CLI).


## 🧱 Struktura projektu

Pliki:

- weather_client.py — klient API, testowalny, z Session i walidacją.
- main.py — warstwa CLI: argumenty, obsługa błędów, exit codes.
- tests/test_weather_client.py — testy logiki klienta (mock Session).
- tests/test_main.py — testy CLI (patch WeatherClient + sys.argv).

## 🔧 Założenia techniczne

### WeatherClient:
- używa requests.Session oraz nagłówków,
- requester pattern → możliwość mockowania całego requests,
- walidacja wejścia: None, pusty string, nie-string,
- budowanie URL,
- obsługa raise_for_status(),
- walidacja JSON poprzez porównanie zbiorów:
  required <= data.keys()
- zgłaszane wyjątki: ValueError, HTTPError, ConnectionError, Exception.

### CLI (main.py):
- pobiera nazwę miasta z argumentów,
- wywołuje WeatherClient,
- obsługuje wyjątki:
  - ValueError → exit code 1 (błąd użytkownika)
  - Exception → exit code 2 (błąd systemowy / API)
  - sukces → exit code 0

### Testy:
- izolowane dzięki mockom,
- patchowanie importu WeatherClient w module main,
- patch sys.argv do symulacji wywołań CLI,
- capsys do wychwycenia stdout.

## 🧪 Testy jednostkowe

Zestaw obejmuje wszystkie kluczowe scenariusze:

### WeatherClient:
- poprawne pobranie danych (happy path),
- HTTPError,
- ConnectionError,
- ValueError przy zbyt małej liczbie pól JSON,
- ValueError przy złym wejściu,
- json() → ValueError przy uszkodzonym JSON.

### main.py (CLI):
- happy path → exit 0,
- ValueError → exit 1,
- Exception → exit 2,
- patchowanie WeatherClient,
- patchowanie sys.argv,
- przechwycenie stdout przez capsys.

Testy są szybkie, deterministyczne i nie korzystają z internetu.

---

## ▶️ Przykład użycia

Użytkownik:

    python main.py Poznań

CLI:

    Pobieram dane pogodowe dla miasta: Poznań
    Wynik: {...}

---

## 🧠 Kluczowe decyzje architektoniczne

- Oddzielenie CLI od klienta API → testowalność.
- Session zamiast requests.get → profesjonalny standard.
- requester pattern → pełne mockowanie bez sieci.
- Exit codes jak w prawdziwych narzędziach UNIX.
- Walidacja JSON przez zbiór wymaganych pól:
      required <= data.keys()

## 🧠 Co ten projekt pokazuje?

Projekt demonstruje umiejętności kluczowe dla pracy w backend / API development:

### ✔ Testowalność
- mockowanie Session,
- mockowanie klas importowanych w CLI,
- użycie side_effect / return_value,
- testowanie błędów i edge cases.

### ✔ Architektura
- warstwa CLI oddzielona od logiki biznesowej,
- czysty przepływ danych,
- jasna semantyka błędów (0/1/2),
- wstrzykiwanie zależności.

### ✔ Jakość kodu
- minimalizm + czytelność,
- poprawne użycie argparse,
- walidacja wejścia i JSON,
- przejrzyste komunikaty.

To projekt, który pokazuje, że potrafię tworzyć
**prawdziwe, testowalne narzędzia używane w praktyce** —
dokładnie to, czego oczekują zespoły backendowe.

---

## 🏁 Podsumowanie

Weather CLI to:
- mały, ale w pełni zawodowy projekt,
- z testami, architekturą i praktykami,
- który jest świetną częścią portfolio.

Pokazuje, że rozumiem:
- API clients,
- testy jednostkowe,
- CLI tools,
- dobrą architekturę,
- mockowanie zewnętrznych zależności.


