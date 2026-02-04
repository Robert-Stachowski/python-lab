import argparse
from pathlib import Path


parser = argparse.ArgumentParser(prog="Mini Explorer CLI")
parser.add_argument("path", help= "path → ścieżka do katalogu lub pliku")
parser.add_argument("--count","-c",action="store_true", help="→ wypisz liczbę plików w katalogu.")
parser.add_argument("--list", "-l", action="store_true",help=" → wypisz zawartość katalogu (nazwy).")
parser.add_argument("--ext","-e",help="→ filtruj tylko pliki o danym rozszerzeniu (np. .txt, .py).")
parser.add_argument("--info","-i", action="store_true",help="→ jeśli path wskazuje na plik → wypisz: * nazwę * rozszerzenie * rozmiar pliku w bajtach * czy jest plikiem, czy katalogiem")



def main():
    args = parser.parse_args()
    target_dir = Path(args.path)
    try:
        if not target_dir.exists():
            print("The target directory doesn't exist")
            raise SystemExit(1)
        if target_dir.is_dir():
            sample_path = target_dir / "example.txt"
            print(sample_path)
# print(sample_path)  # zostawione jako przykład użycia operatora /
            if args.info:
                print("--info działa tylko dla plików.")
                return 2
            elif args.count:
                files = [f for f in target_dir.iterdir() if f.is_file()]
                print(len(files))
            elif args.list:
                for entry in target_dir.iterdir():
                    print(entry.name)
            elif args.ext:
                for entry in target_dir.iterdir():
                    if entry.is_file() and entry.suffix == args.ext:
                        print(entry.name)
            else:
                parser.print_help()
                return 2
        elif target_dir.is_file():
            if args.count or args.list or args.ext:
                print("Flagi --count, --list i --ext działają tylko na katalogach.")
                return 2
            if args.info:
                print("Nazwa:", target_dir.name)
                print("Rozszerzenie:", target_dir.suffix)
                print("Rozmiar (bajty):", target_dir.stat().st_size)
                print("Czy plik?", target_dir.is_file())
                print("Czy katalog?", target_dir.is_dir())
                return 0
            parser.print_help()
            return 2
    except Exception as e:
        print(f"Nieoczekiwany błąd: {e}")
        return 1
    

if __name__ == "__main__":
    raise SystemExit(main())


"""


### Importy

**1.** `import argparse`
Importujemy moduł `argparse`, który służy do budowania interfejsów wiersza poleceń (CLI). Dzięki niemu możemy zdefiniować argumenty, flagi i automatycznie generować `--help`.

**2.** `from pathlib import Path`
Importujemy klasę `Path` z modułu `pathlib`. Umożliwia ona wygodną, obiektową pracę ze ścieżkami plików i katalogów (zamiast używania `os.path` i gołych stringów).

---

### Tworzenie parsera i definiowanie argumentów

**3.** `parser = argparse.ArgumentParser(prog="Mini Explorer CLI")`
Tworzymy obiekt parsera argumentów.
Parametr `prog` ustawia nazwę programu, która będzie wyświetlana w komunikatach pomocy (`Mini Explorer CLI` zamiast samej nazwy pliku).

**4.** `parser.add_argument("path", help= "path → ścieżka do katalogu lub pliku")`
Definiujemy **argument pozycyjny** `path`.
Użytkownik MUSI go podać. Będzie to ścieżka do katalogu albo do pliku.
`help` opisuje ten argument i pojawi się w `--help`.

**5.** `parser.add_argument("--count","-c",action="store_true", help="→ wypisz liczbę plików w katalogu.")`
Dodajemy **opcjonalną flagę** `--count` (alias `-c`).
`action="store_true"` oznacza: jeśli flaga jest podana, to `args.count == True`, jeśli nie – `False`.
Flaga ta ma w zamierzeniu zliczać pliki w katalogu i wypisywać ich liczbę.

**6.** `parser.add_argument("--list", "-l", action="store_true",help=" → wypisz zawartość katalogu (nazwy).")`
Dodajemy flagę `--list` (alias `-l`).
Znów `store_true` → bool w `args.list`.
Ta flaga ma wypisywać zawartość katalogu: nazwy elementów (pliki / podkatalogi).

**7.** `parser.add_argument("--ext","-e",help="→ filtruj tylko pliki o danym rozszerzeniu (np. .txt, .py).")`
Dodajemy opcję `--ext` (alias `-e`), tym razem **bez** `action="store_true"`.
Tutaj użytkownik ma podać WARTOŚĆ, np. `.py` albo `.txt`.
`args.ext` będzie stringiem zawierającym rozszerzenie użyte do filtrowania.

**8.** `parser.add_argument("--info","-i", action="store_true",help="→ jeśli path wskazuje na plik → wypisz: * nazwę * rozszerzenie * rozmiar pliku w bajtach * czy jest plikiem, czy katalogiem")`
Dodajemy flagę `--info` (alias `-i`).
Znowu `store_true` → `args.info` to bool.
Jeśli `path` wskazuje na plik i ta flaga jest podana, program ma wypisać szczegółowe informacje o pliku (nazwa, rozszerzenie, rozmiar, itp.).

---

### Parsowanie argumentów i przygotowanie ścieżki

**10.** `args = parser.parse_args()`
Wywołujemy `parse_args()`, żeby odczytać argumenty podane w wierszu poleceń.
Wynik trafia do obiektu `args`, np. `args.path`, `args.count`, `args.list`, `args.ext`, `args.info`.

**11.** `target_dir = Path(args.path)`
Tworzymy obiekt `Path` na podstawie stringa przekazanego jako `path`.
`target_dir` może być katalogiem albo plikiem – dowiemy się tego później za pomocą `is_dir()` / `is_file()`.

---

### Funkcja `main()` – logika programu

**13.** `def main():`
Definiujemy funkcję `main()`, która zawiera główną logikę programu.
Na końcu pliku funkcja ta będzie wywołana, jeśli skrypt uruchomiono jako program.

**14.** `    try:`
Zaczynamy blok `try`.
Jeśli w trakcie działania pojawi się jakiś nieprzewidziany błąd (wyjątek), przechwycimy go w `except` i wypiszemy komunikat zamiast ścinać program tracebackiem.

---

### Walidacja ścieżki

**15.** `        if not target_dir.exists():`
Sprawdzamy, czy ścieżka wskazana przez użytkownika w ogóle istnieje w systemie plików.

**16.** `            print("The target directory doesn't exist")`
Jeśli nie istnieje, wypisujemy komunikat o błędzie.

**17.** `            raise SystemExit(1)`
Kończymy działanie programu z kodem wyjścia `1` (błąd).
`SystemExit(1)` to standardowy sposób na zakończenie programu z konkretnym kodem.

---

### Gdy `path` wskazuje na katalog

**18.** `        if target_dir.is_dir():`
Sprawdzamy, czy `target_dir` jest katalogiem (`is_dir()` zwraca `True/False`).
Jeśli to katalog, wykonamy logikę zależną od flag: `--info`, `--count`, `--list`, `--ext`.

**19.** `            if args.info:`
Sprawdzamy, czy użytkownik podał `--info` razem z katalogiem.

**20.** `                print("--info działa tylko dla plików.")`
Jeśli tak – to błąd logiczny (według założeń programu `--info` jest tylko dla plików).
Wypisujemy jasny komunikat, że `--info` działa tylko dla plików.

**21.** `                return 2`
Kończymy funkcję `main()` z kodem `2`.
Kod `2` można tu traktować jako „nieprawidłowe użycie programu / złe połączenie flag”.

---

**22.** `            elif args.count:`
Jeśli nie było `--info`, sprawdzamy, czy podana została flaga `--count`.
To znaczy: użytkownik chce policzyć pliki w katalogu.

**23.** `                files = [f for f in target_dir.iterdir() if f.is_file()]`
Tworzymy listę `files` z elementów zwróconych przez `target_dir.iterdir()`,
ale filtrujemy tylko te, które są plikami (`f.is_file()`).
`iterdir()` iteruje po zawartości katalogu (pliki + podkatalogi).

**24.** `                print(len(files))`
Wypisujemy liczbę plików znalezionych w katalogu.
`len(files)` to liczba elementów w liście `files`.

---

**25.** `            elif args.list:`
Jeśli nie było `--info` ani `--count`, sprawdzamy, czy jest flaga `--list`.
Wtedy użytkownik chce tylko zobaczyć zawartość katalogu.

**26.** `                for entry in target_dir.iterdir():`
Iterujemy po wszystkich elementach w katalogu: plikach i podkatalogach.
`entry` to obiekt `Path` reprezentujący każdy element.

**27.** `                    print(entry.name)`
Dla każdego elementu wypisujemy jego `name` (czyli samą nazwę, bez pełnej ścieżki).

---

**28.** `            elif args.ext:`
Jeśli nie było wcześniejszych flag, sprawdzamy, czy podano `--ext`.
Oznacza to, że użytkownik chce przefiltrować pliki po rozszerzeniu.

**29.** `                for entry in target_dir.iterdir():`
Iterujemy po zawartości katalogu.

**30.** `                    if entry.is_file() and entry.suffix == args.ext:`
Dla każdego elementu sprawdzamy dwa warunki naraz:

* `entry.is_file()` – czy to plik (ignorujemy katalogi)
* `entry.suffix == args.ext` – czy rozszerzenie pliku (np. `.py`) jest takie, jak użytkownik podał w `--ext`.

**31.** `                        print(entry.name)`
Jeśli warunek jest spełniony, wypisujemy nazwę pliku.

---

**32.** `            else:`
Ten `else` wykona się, jeśli:

* ścieżka była katalogiem,
* ale użytkownik nie podał żadnej z obsługiwanych flag: `--info`, `--count`, `--list`, `--ext`.

**33.** `                parser.print_help()`
Wypisujemy automatycznie wygenerowaną pomoc (opis argumentów i flag).
To dobra praktyka, gdy użytkownik uruchomi program w „bezsensowny” sposób.

**34.** `                return 2`
Zwracamy kod `2` jako informację o nieprawidłowym użyciu.

---

### Gdy `path` wskazuje na plik

**35.** `        if target_dir.is_file():`
Drugi główny przypadek: sprawdzamy, czy `target_dir` jest plikiem.
Jeśli tak – obsługujemy logikę dedykowaną plikom.

**36.** `            if args.count or args.list or args.ext:`
Jeśli do pliku zostały użyte flagi typowe dla katalogu (`--count`, `--list`, `--ext`),
to jest to niepoprawne użycie programu.

**37.** `                print("Flagi --count, --list i --ext działają tylko na katalogach.")`
Wypisujemy jasny komunikat, że te flagi mają sens tylko dla katalogów.

**38.** `                return 2`
Kończymy z kodem `2` (błędne użycie flag).

---

**39.** `            if args.info:`
Jeśli nie użyto złych flag katalogowych, sprawdzamy, czy jest flaga `--info`.
To jest poprawna flaga dla pliku.

**40.** `                print("Nazwa:", target_dir.name)`
Wypisujemy nazwę pliku (`name` – bez ścieżki).

**41.** `                print("Rozszerzenie:", target_dir.suffix)`
Wypisujemy rozszerzenie pliku (`suffix`), np. `.py`, `.txt`.

**42.** `                print("Rozmiar (bajty):", target_dir.stat().st_size)`
Pobieramy informację o pliku za pomocą `stat()` i wypisujemy pole `st_size`, czyli jego rozmiar w bajtach.

**43.** `                print("Czy plik?", target_dir.is_file())`
Dla pełni informacji – wypisujemy, czy `target_dir` jest plikiem (powinno być `True`).

**44.** `                print("Czy katalog?", target_dir.is_dir())`
Dodatkowo – czy jest katalogiem (powinno być `False` dla zwykłego pliku).

**45.** `                return 0`
Zwracamy `0`, czyli „wszystko OK, wykonane poprawnie”.

---

**46.** `            parser.print_help()`
Jeśli ścieżka jest plikiem, ale użytkownik nie podał żadnej sensownej flagi (np. uruchomił tylko `python explorer.py somefile.py` bez `--info`),
to wyświetlamy pomoc, bo program nie wie, co ma zrobić.

**47.** `            return 2`
Zwracamy kod `2` – znowu oznacza to niepoprawne użycie programu (brak flag przy pliku).

---

### Obsługa nieoczekiwanych wyjątków

**48.** `    except Exception as e:`
Jeśli w bloku `try` wystąpi jakikolwiek nieobsłużony wcześniej wyjątek, przechwytujemy go tutaj.
To zabezpieczenie, żeby użytkownik nie widział brzydkiego tracebacka.

**49.** `        print(f"Nieoczekiwany błąd: {e}")`
Wypisujemy czytelny komunikat o tym, że wystąpił nieoczekiwany błąd, razem z treścią wyjątku (`e`).

**50.** `        return 1`
Zwracamy kod `1`, jako informację, że program zakończył się z błędem wykonania.

---

### Uruchamianie `main()` przy starcie skryptu

**53.** `if __name__ == "__main__":`
Ten warunek sprawdza, czy plik został uruchomiony bezpośrednio (np. `python explorer.py`), a nie zaimportowany jako moduł.
Tylko w takim przypadku chcemy naprawdę wykonać `main()`.

**54.** `    raise SystemExit(main())`
Wywołujemy funkcję `main()` i zwracamy jej wartość jako kod wyjścia programu, używając `SystemExit(...)`.
Dzięki temu:

* jeśli `main()` zwróci `0` → program kończy się sukcesem,
* jeśli `1` albo `2` → system dostaje informację o błędach / złym użyciu.




"""