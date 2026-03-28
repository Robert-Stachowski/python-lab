# Notatki techniczne: main.py


Dokumentacja techniczna:

---

## Importy

```python
import argparse
from weather_client import WeatherClient
```

`argparse` — biblioteka do parsowania argumentów z linii poleceń.

`WeatherClient` importujemy z osobnego pliku bo `main.py` to "dyrygent" — nie zawiera logiki HTTP,
tylko orchestruje: pobierz argumenty, wywołaj klienta, wyświetl wynik.
Logika HTTP siedzi w `WeatherClient`.

To zasada **separation of concerns** — każdy plik ma jedną odpowiedzialność.

---

## `build_parser()`

```python
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="Weather client",
        description="Pobiera aktualne dane pogodowe dla podanego miasta."
    )
    parser.add_argument("city_name", help="Pogoda dla konkretnego miasta")
    return parser
```

Wydzielona do osobnej funkcji z dwóch powodów:
1. **Czytelność** — `main()` jest czysty, bez szczegółów konfiguracji parsera
2. **Testowalność** — `test_build_parser()` może przetestować parser w izolacji bez uruchamiania całego `main()`

---

## `main() -> int`

```python
def main() -> int:
```

Zwraca `int` bo exit codes informują system operacyjny o wyniku działania programu:

```
return 0  — sukces
return 1  — ValueError (błąd użytkownika: złe dane, brak pól w JSON)
return 2  — Exception (błąd krytyczny: sieć, API, coś nieoczekiwanego)
```

---

```python
parser = build_parser()
args = parser.parse_args()
```

`parse_args()` czyta `sys.argv` — to co użytkownik wpisał w terminalu — i zwraca obiekt z atrybutami.

Jeśli użytkownik wpisał `python main.py Warszawa`, to `args.city_name` zawiera `"Warszawa"`.
Nazwa atrybutu pochodzi z `parser.add_argument("city_name", ...)`.

---

```python
client = WeatherClient()
```

Tworzymy instancję bez podawania `requester` — klasa sama użyje prawdziwego `requests`.
To jest produkcyjne użycie, w przeciwieństwie do testów gdzie podajemy `Mock()`.

---

```python
print(f"Pobieram dane pogodowe dla miasta: {args.city_name}")
```

Print jest **przed** wywołaniem API — UX. Użytkownik widzi od razu że coś się dzieje.
Gdyby był po — przy wolnym połączeniu program wyglądałby jakby się zawiesił.

---

## Obsługa błędów

```python
try:
    data = client.get_city_weather(args.city_name)
except ValueError as e:
    print(f"błąd: {e}")
    return 1
except Exception as e:
    print(f"błąd krytyczny: {e}")
    return 2
```

**Dlaczego `ValueError` przed `Exception`?**

`ValueError` jest podklasą `Exception`. Gdyby `Exception` było pierwsze — złapałoby wszystko
włącznie z `ValueError` i nigdy nie dotarłbyś do drugiego `except`. `ValueError` byłby martwy.

Python sprawdza `except` od góry i zatrzymuje się przy pierwszym pasującym.
Zawsze — bardziej szczegółowy wyjątek przed bardziej ogólnym.

---

## Wyświetlenie wyniku

```python
print(f"Miasto:      {data['city']}")
print(f"Temperatura: {data['temp_c']}°C")
print(f"Pogoda:      {data['condition']}")
return 0
```

Dostęp przez `data['klucz']` jest bezpieczny — `WeatherClient` gwarantuje że te klucze istnieją
(walidacja `required <= data.keys()` rzuciłaby `ValueError` wcześniej).

---

## `if __name__ == "__main__"`

```python
if __name__ == "__main__":
    raise SystemExit(main())
```

**`SystemExit(main())`** — `main()` zwraca `int`, `SystemExit` przekazuje tę liczbę
do systemu operacyjnego jako exit code.

**`if __name__ == "__main__"`** — blok wykonuje się tylko gdy uruchamiasz plik bezpośrednio:
```
python main.py Warszawa   →  __name__ == "__main__"  →  blok się wykonuje
```

Gdy importujesz moduł w teście:
```python
from main import main, build_parser   →  __name__ == "main"  →  blok się NIE wykonuje
```

Dzięki temu testy mogą importować `main` bez ryzyka że `SystemExit` odpali się przy imporcie.

---

## Przepływ end-to-end

```
python main.py Warszawa
    ↓
build_parser() + parse_args() → args.city_name = "Warszawa"
    ↓
WeatherClient() — instancja z prawdziwym requests
    ↓
print "Pobieram dane..." (natychmiast, przed requestem)
    ↓
client.get_city_weather("Warszawa")
    ↓
    sukces → print Miasto / Temperatura / Pogoda → return 0
    ValueError → print błąd → return 1
    Exception → print błąd krytyczny → return 2
    ↓
SystemExit(0/1/2) → exit code do systemu operacyjnego
```
