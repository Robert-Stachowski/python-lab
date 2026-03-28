# Notatki techniczne: Mini Explorer CLI

Dokumentacja mini explorer cli. Projekt: narzędzie do eksploracji systemu plików z poziomu terminala.

---

## 1. Importy (linie 1-2)

```python
import argparse
from pathlib import Path
```

### `argparse`
Moduł standardowej biblioteki do budowania interfejsów CLI. Daje nam:
- automatyczne **parsowanie** argumentów z `sys.argv`
- generowanie `--help`
- walidację typów i wymaganych argumentów

**Co to znaczy parsowanie?**
Kiedy piszesz w terminalu:
```bash
python mini_explorer_cli.py . --count
```
Python widzi to jako surową listę stringów:
```python
["mini_explorer_cli.py", ".", "--count"]
```
Parsowanie = zamiana tej listy na sensowny obiekt z nazwanymi polami:
```python
args.path  = "."
args.count = True
args.list  = False
args.ext   = None
args.info  = False
```
Teraz możesz pisać `if args.count:` zamiast ręcznie przeszukiwać listę stringów.

### `from pathlib import Path`
Importujemy tylko klasę `Path` z modułu `pathlib`. Nowoczesne (Python 3.4+) obiektowe podejście do pracy ze ścieżkami — zamiast starszego `os.path` operującego na gołych stringach.

```python
# os.path — stary styl
import os
os.path.join("/katalog", "plik.txt")

# pathlib — nowy styl
Path("/katalog") / "plik.txt"
```

---

## 2. `create_parser()` (linie 5-12)

```python
def create_parser():
    parser = argparse.ArgumentParser(prog="Mini Explorer CLI")
    parser.add_argument("path", help="ścieżka do katalogu lub pliku")
    parser.add_argument("--count", "-c", action="store_true", help="wypisz liczbę plików w katalogu")
    parser.add_argument("--list", "-l", action="store_true", help="wypisz zawartość katalogu (nazwy)")
    parser.add_argument("--ext", "-e", help="filtruj pliki po rozszerzeniu (np. .txt, .py)")
    parser.add_argument("--info", "-i", action="store_true", help="wypisz informacje o pliku")
    return parser
```

### `ArgumentParser(prog="Mini Explorer CLI")`
Tworzymy obiekt parsera. `prog` to nazwa programu wyświetlana w `--help`.
Bez tego byłoby `mini_explorer_cli.py`.

### Argument pozycyjny vs opcjonalny

```python
parser.add_argument("path", ...)     # pozycyjny — WYMAGANY, bez myślników
parser.add_argument("--count", ...)  # opcjonalny — niewymagany, z myślnikiem
```

Użytkownik **musi** podać `path`. Reszta jest opcjonalna.

### Alias (`"-c"` obok `"--count"`)
Użytkownik może pisać zamiennie:
```bash
python mini_explorer_cli.py . --count
python mini_explorer_cli.py . -c
```

### `action="store_true"`
Flaga bez wartości. Obecność = `True`, brak = `False`.

Porównaj z `--ext` — tam **nie ma** `action="store_true"`, bo użytkownik podaje wartość:
```bash
python mini_explorer_cli.py . --ext .py   # args.ext = ".py"
python mini_explorer_cli.py . --count     # args.count = True
```

### `return parser`
Funkcja zwraca gotowy parser. Dzięki temu parser nie jest zmienną globalną — tworzony jest na żądanie, wewnątrz funkcji.

---

## 3. Początek `main()` (linie 15-18)

```python
def main():
    parser = create_parser()
    args = parser.parse_args()
    path = Path(args.path)
```

### `def main()`
Konwencja — logika programu siedzi w funkcji `main()`, nie na poziomie globalnym. Dzięki temu:
- kod można zaimportować bez efektów ubocznych
- kod można przetestować (wywołujesz `main()` w teście)
- kod jest czytelniejszy

### `parser = create_parser()`
Wywołujemy funkcję z góry — dostajemy gotowy parser z zarejestrowanymi argumentami.

### `args = parser.parse_args()`
Parser czyta `sys.argv` i zwraca obiekt `Namespace` z polami:
```python
args.path   # string — ścieżka podana przez użytkownika
args.count  # bool
args.list   # bool
args.ext    # string lub None
args.info   # bool
```

### `path = Path(args.path)`
`args.path` to zwykły string, np. `"."` albo `"C:/Users/Robert"`.
`Path(...)` zamienia go w obiekt Path — dopiero teraz możemy robić operacje systemu plików:

```python
path.exists()    # czy istnieje?
path.is_dir()    # czy katalog?
path.is_file()   # czy plik?
path.iterdir()   # lista zawartości katalogu
path.name        # sama nazwa (bez ścieżki)
path.suffix      # rozszerzenie, np. ".py"
path.stat()      # metadane pliku (rozmiar, daty)
```

Na samym stringu `"."` nic z tego nie zadziała.

---

## 4. Walidacja ścieżki + blok `try/except` (linie 19-22)

```python
try:
    if not path.exists():
        print("The target directory doesn't exist")
        raise SystemExit(1)
```

### `try:`
Cała logika programu siedzi w bloku `try`. Jeśli gdzieś wyskoczy nieoczekiwany wyjątek — przechwytujemy go w `except` na dole i wypisujemy czytelny komunikat zamiast brzydkiego tracebacka.

### `path.exists()`
Metoda obiektu `Path`. Sprawdza czy ścieżka w ogóle istnieje w systemie plików — nieważne czy to plik czy katalog. Zwraca `True` lub `False`.

`not path.exists()` — negacja: jeśli **nie** istnieje.

### `raise SystemExit(1)`
Kończymy program z kodem wyjścia `1`.

Trzy kody wyjścia używane w tym projekcie:

| Kod | Znaczenie | Kiedy |
|-----|-----------|-------|
| `0` | sukces | operacja wykonana poprawnie |
| `1` | błąd | ścieżka nie istnieje, nieoczekiwany wyjątek |
| `2` | złe użycie | zła kombinacja flag |

`raise SystemExit(1)` zamiast `return 1` — bo jesteśmy wewnątrz `try`, a `return` tylko wyszedłby z funkcji. Tu chcemy natychmiastowego zakończenia programu z konkretnym kodem.

---

## 5. Logika dla katalogu (linie 23-42)

```python
if path.is_dir():
    if args.info:
        print("--info działa tylko dla plików.")
        return 2
    elif args.count:
        files = [f for f in path.iterdir() if f.is_file()]
        print(len(files))
        return 0
    elif args.list:
        for entry in path.iterdir():
            print(entry.name)
        return 0
    elif args.ext:
        for entry in path.iterdir():
            if entry.is_file() and entry.suffix == args.ext:
                print(entry.name)
        return 0
    else:
        parser.print_help()
        return 2
```

### `path.is_dir()`
Sprawdzamy czy ścieżka to katalog. Jeśli tak — wchodzimy w ten blok.

### `if args.info: ... return 2`
`--info` ma sens tylko dla plików. Jeśli użytkownik poda katalog + `--info` — informujemy o błędzie i kończymy z kodem `2` (złe użycie).

### `[f for f in path.iterdir() if f.is_file()]`
List comprehension — w jednej linii tworzymy listę plików z katalogu.

Rozbite na części:
```python
for f in path.iterdir()  # iteruj po wszystkich elementach katalogu
if f.is_file()           # weź tylko pliki (pomiń podkatalogi)
```

`path.iterdir()` zwraca obiekty `Path` — zarówno pliki jak i podkatalogi. Filtrujemy tylko pliki przez `f.is_file()`.

`print(len(files))` — `len()` zwraca liczbę elementów listy.

### `entry.name`
Sama nazwa elementu bez pełnej ścieżki:
```
entry = Path("F:/projekty/mini_explorer_cli.py")
entry.name  →  "mini_explorer_cli.py"
```

### `entry.suffix == args.ext`
`entry.suffix` to rozszerzenie pliku jako string, np. `".py"`, `".txt"`.
Porównujemy z tym co podał użytkownik w `--ext`.

Uwaga — użytkownik musi podać rozszerzenie z kropką:
```bash
python mini_explorer_cli.py . --ext .py   ✓
python mini_explorer_cli.py . --ext py    ✗  (nie znajdzie nic)
```

### `else: parser.print_help()`
Jeśli ścieżka jest katalogiem ale użytkownik nie podał żadnej flagi — wyświetlamy pomoc zamiast cicho nic nie robić.

---

## 6. Logika dla pliku (linie 43-55)

```python
elif path.is_file():
    if args.count or args.list or args.ext:
        print("Flagi --count, --list i --ext działają tylko na katalogach.")
        return 2
    if args.info:
        print("Nazwa:", path.name)
        print("Rozszerzenie:", path.suffix)
        print("Rozmiar (bajty):", path.stat().st_size)
        print("Czy plik?", path.is_file())
        print("Czy katalog?", path.is_dir())
        return 0
    parser.print_help()
    return 2
```

### `elif path.is_file()`
`elif` — bo wcześniej sprawdziliśmy `is_dir()`. Jeśli ścieżka nie była katalogiem, sprawdzamy czy jest plikiem.

### `if args.count or args.list or args.ext:`
Walidacja — te trzy flagi mają sens tylko dla katalogów. `or` — wystarczy że jedna z flag jest podana żeby warunek był `True`.

### `path.name`
Sama nazwa pliku bez ścieżki:
```
Path("F:/projekty/mini_explorer_cli.py").name  →  "mini_explorer_cli.py"
```

### `path.suffix`
Rozszerzenie pliku:
```
Path("mini_explorer_cli.py").suffix  →  ".py"
Path("dane.tar.gz").suffix           →  ".gz"   (tylko ostatnie!)
```

### `path.stat().st_size`
`stat()` zwraca obiekt z metadanymi pliku. `st_size` to rozmiar w bajtach.

Inne pola `stat()` których tu nie używamy:
```python
path.stat().st_mtime  # czas ostatniej modyfikacji (timestamp)
path.stat().st_ctime  # czas utworzenia
```

### `path.is_file()` i `path.is_dir()` w `--info`
Wiemy już że to plik — więc `is_file()` zawsze zwróci `True`, a `is_dir()` zawsze `False`. Wypisujemy to dla pokazania że te metody istnieją — cel edukacyjny.

---

## 7. Obsługa wyjątków (linie 56-58)

```python
except Exception as e:
    print(f"Nieoczekiwany błąd: {e}")
    return 1
```

### `except Exception as e:`
Przechwytujemy każdy wyjątek który dziedziczy po `Exception`. `as e` przypisuje obiekt wyjątku do zmiennej `e` — żeby móc wypisać jego treść.

Czego **nie** przechwytuje `Exception`:
```python
SystemExit        # zakończenie programu — dziedziczy po BaseException
KeyboardInterrupt # Ctrl+C — też po BaseException
```

To celowe — `SystemExit` rzucany wyżej przy `not path.exists()` **nie** zostanie tu złapany. Wyjdzie z programu tak jak chcemy.

### `f"Nieoczekiwany błąd: {e}"`
f-string — wstawiamy treść wyjątku do stringa. Użytkownik widzi czytelny komunikat zamiast tracebacka.

Bez `try/except`:
```
Traceback (most recent call last):
  ...
PermissionError: [Errno 13] Permission denied: '/root'
```

Z `try/except`:
```
Nieoczekiwany błąd: [Errno 13] Permission denied: '/root'
```

---

## 8. Punkt wejścia programu (linie 61-62)

```python
if __name__ == "__main__":
    raise SystemExit(main())
```

### `if __name__ == "__main__":`
Każdy plik Python ma zmienną `__name__`. Jej wartość zależy od tego jak plik został uruchomiony:

```python
# uruchomiony bezpośrednio:
python mini_explorer_cli.py .  →  __name__ == "__main__"

# zaimportowany w innym pliku:
import mini_explorer_cli       →  __name__ == "mini_explorer_cli"
```

Dzięki temu `main()` nie wykona się przy imporcie — co jest kluczowe dla testów, bo tam importujemy `create_parser` bez uruchamiania całego programu.

### `raise SystemExit(main())`
Wywołujemy `main()` i przekazujemy jej wynik jako kod wyjścia do systemu operacyjnego.

```python
main() zwraca 0  →  SystemExit(0)  →  program zakończony sukcesem
main() zwraca 1  →  SystemExit(1)  →  błąd
main() zwraca 2  →  SystemExit(2)  →  złe użycie
```

Dlaczego `raise SystemExit(...)` a nie `sys.exit()`? To to samo — `sys.exit()` wewnętrznie też rzuca `SystemExit`. Tutaj robimy to bezpośrednio bez dodatkowego importu `sys`.
