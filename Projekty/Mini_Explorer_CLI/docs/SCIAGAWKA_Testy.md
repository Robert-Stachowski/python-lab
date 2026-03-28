# Ściągawka: Testy — Mini Explorer CLI

Dokumentacja testów linijka po linijce. Testy sprawdzają działanie CLI bez uruchamiania procesu.

---

## Narzędzia pytest używane w testach

| Narzędzie | Co robi |
|-----------|---------|
| `tmp_path` | tworzy tymczasowy katalog na czas testu, automatycznie usuwany po teście |
| `monkeypatch` | podmienia wartości w czasie testu (np. `sys.argv`) — przywracane automatycznie po teście |
| `capsys` | przechwytuje to co program wypisuje przez `print()` |
| `pytest.raises` | sprawdza czy program rzucił oczekiwany wyjątek (np. `SystemExit`) |

---

## Importy

```python
import sys
import pytest
from mini_explorer_cli import main
```

**`import sys`** — potrzebny żeby podmieniać `sys.argv`.

**`import pytest`** — potrzebny do `pytest.raises`.

**`from mini_explorer_cli import main`** — importujemy funkcję `main()` bezpośrednio.
Działa bo w pliku jest `if __name__ == "__main__"` — import nie uruchamia programu.

---

## Jak `monkeypatch` przekazuje dane do `main()`

`main()` nie przyjmuje żadnych argumentów — jej sygnatura to `def main():`.

Dane dostaje **pośrednio** — w środku wywołuje `parser.parse_args()`, które samo sięga do `sys.argv`.

Przepływ:
```
monkeypatch ustawia sys.argv = ["prog", str(tmp_path), "--ext", ".txt"]
        ↓
main() zostaje wywołane
        ↓
parser.parse_args() czyta sys.argv
        ↓
args.path = str(tmp_path)
args.ext  = ".txt"
```

`monkeypatch` nie podstawia nic pod `main()` bezpośrednio — podmienia globalną zmienną `sys.argv`, z której `main()` korzysta wewnętrznie. Dlatego musi być ustawiony **przed** wywołaniem `main()`.

---

## Wzorzec każdego testu — AAA

```
Arrange  →  przygotuj dane (utwórz pliki, ustaw sys.argv)
Act      →  wywołaj main()
Assert   →  sprawdź wynik
```

---

## `monkeypatch.setattr` — kluczowy wzorzec

```python
monkeypatch.setattr(sys, "argv", ["prog", str(tmp_path), "--count"])
```

**`monkeypatch.setattr(obiekt, "nazwa_atrybutu", nowa_wartość)`**

Podmienia w obiekcie `sys` atrybut `"argv"` na podaną listę — na czas trwania testu.
Po teście pytest automatycznie przywraca oryginalną wartość.

**Dlaczego to potrzebne?**
Normalnie kiedy piszesz w terminalu:
```bash
python mini_explorer_cli.py . --count
```
Python automatycznie ustawia:
```python
sys.argv = ["mini_explorer_cli.py", ".", "--count"]
```
W teście nie ma terminala — więc sami ustawiamy `sys.argv` ręcznie.

**Co jest w liście:**
```python
["prog",          # argv[0] — nazwa skryptu, argparse to ignoruje
 str(tmp_path),   # argv[1] — ścieżka do katalogu (Path zamieniamy na string)
 "--count"]       # argv[2] — flaga
```

`str(tmp_path)` — bo `tmp_path` to obiekt `Path`, a `sys.argv` trzyma stringi.

---

## `capsys.readouterr()` — przechwytywanie outputu

```python
captured = capsys.readouterr()
assert captured.out.strip() == "3"
```

**`capsys.readouterr()`** — przechwytuje wszystko co poszło przez `print()`.
- `captured.out` — stdout (to co `print()` wypisuje normalnie)
- `captured.err` — stderr (błędy)

**`.strip()`** — usuwa `\n` na końcu stringa przed porównaniem.

---

## Test 1 — `test_count_files`

```python
def test_count_files(tmp_path, monkeypatch, capsys):
    (tmp_path / "a.txt").write_text("hello")
    (tmp_path / "b.txt").write_text("world")
    (tmp_path / "c.py").write_text("code")

    monkeypatch.setattr(sys, "argv", ["prog", str(tmp_path), "--count"])
    result = main()

    captured = capsys.readouterr()
    assert result == 0
    assert captured.out.strip() == "3"
```

**`tmp_path / "a.txt"`** — operator `/` na obiekcie `Path` skleja ścieżkę.

**`.write_text("hello")`** — tworzy plik z treścią. Treść nie ma znaczenia — chodzi tylko o to żeby pliki istniały.

**`assert result == 0`** — sprawdzamy kod wyjścia (sukces).

**`assert captured.out.strip() == "3"`** — program powinien wypisać liczbę plików.

---

## Test 2 — `test_list_files`

```python
def test_list_files(tmp_path, monkeypatch, capsys):
    (tmp_path / "a.txt").write_text("hello")
    (tmp_path / "b.py").write_text("code")

    monkeypatch.setattr(sys, "argv", ["prog", str(tmp_path), "--list"])
    result = main()

    captured = capsys.readouterr()
    assert result == 0
    names = captured.out.strip().split("\n")
    assert "a.txt" in names
    assert "b.py" in names
```

**`captured.out.strip().split("\n")`** — dzielimy cały output na listę nazw.
Zamiast porównywać cały string naraz, sprawdzamy każdą nazwę osobno.

Dlaczego nie `== "a.txt\nb.py"`?
Bo `iterdir()` nie gwarantuje kolejności — pliki mogą wyjść w dowolnej kolejności.
`in names` jest odporne na kolejność, porównanie całego stringa nie.

## Test 3 — `test_ext_filter`

```python
def test_ext_filter(tmp_path, monkeypatch, capsys):
    (tmp_path / "a.txt").write_text("hello")
    (tmp_path / "b.txt").write_text("world")
    (tmp_path / "c.py").write_text("code")

    monkeypatch.setattr(sys, "argv", ["prog", str(tmp_path), "--ext", ".txt"])
    result = main()

    captured = capsys.readouterr()
    assert result == 0
    names = captured.out.strip().split("\n")
    assert "a.txt" in names
    assert "b.txt" in names
    assert "c.py" not in names
```

**`assert "c.py" not in names`** — sprawdzamy nie tylko że właściwe pliki są w wyniku,
ale też że plik z innym rozszerzeniem **nie** pojawił się.
Test powinien weryfikować zarówno co jest, jak i czego nie ma.

## Test 4 — `test_info_file`

```python
def test_info_file(tmp_path, monkeypatch, capsys):
    f = tmp_path / "test.py"
    f.write_text("hello")

    monkeypatch.setattr(sys, "argv", ["prog", str(f), "--info"])
    result = main()

    captured = capsys.readouterr()
    assert result == 0
    assert "test.py" in captured.out
    assert ".py" in captured.out
    assert "Czy plik? True" in captured.out
```

**`f = tmp_path / "test.py"`** — tym razem podajemy ścieżkę do pliku, nie katalogu.

**`str(f)`** — zamieniamy obiekt Path na string dla `sys.argv`.

**Asercje na fragmentach** — nie porównujemy całego outputu, bo rozmiar pliku będzie za każdym razem inny. Sprawdzamy tylko kluczowe fragmenty: nazwę, rozszerzenie, i czy `is_file()` zwróciło `True`.

## Test 5 — `test_nonexistent_path`

```python
def test_nonexistent_path(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["prog", "/nonexistent/path/xyz"])
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code == 1
```

**Brak `tmp_path` i `capsys`** — nie tworzymy plików ani nie sprawdzamy outputu. Fixture dodajemy tylko gdy potrzebujemy.

**`pytest.raises(SystemExit)`** — w kodzie przy nieistniejącej ścieżce robimy `raise SystemExit(1)`, nie `return 1`. Zwykłe `assert result == 1` by nie zadziałało — `SystemExit` przerywa wykonanie zanim `main()` cokolwiek zwróci. `pytest.raises` przechwytuje ten wyjątek.

**`exc.value.code`** — sprawdzamy konkretny kod wyjścia (`1`), nie tylko że wyjątek w ogóle wystąpił.

## Test 6 — `test_wrong_flag_on_file`

```python
def test_wrong_flag_on_file(tmp_path, monkeypatch):
    f = tmp_path / "test.txt"
    f.write_text("hello")

    monkeypatch.setattr(sys, "argv", ["prog", str(f), "--count"])
    result = main()

    assert result == 2
```

**Brak `capsys`** — nie interesuje nas co wypisał program, tylko kod wyjścia.
Sprawdzamy że `--count` użyte na pliku zwraca `2` (złe użycie).

## Test 7 — `test_info_on_dir`

```python
def test_info_on_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["prog", str(tmp_path), "--info"])
    result = main()

    assert result == 2
```

**Brak tworzenia plików** — sam `tmp_path` jako katalog wystarczy.
Sprawdzamy że `--info` użyte na katalogu zwraca `2` (złe użycie).
