# 🧰 CLI Examples & Templates (Python)

Zbiór dwóch praktycznych, w pełni działających przykładów aplikacji CLI w Pythonie.  
Pokazują **dobry styl**, **modularność**, **obsługę błędów**, **argparse**, **pathlib.Path** oraz przygotowanie kodu pod testowanie i patchowanie.

Folder został stworzony jako:
- baza wiedzy na przyszłość,
- materiał rekrutacyjny pokazujący świadomość narzędzi CLI,
- gotowy punkt startowy do budowania własnych narzędzi developerskich.

---

## 📂 Zawartość katalogu

### 1. `cli_template.py` — kompletny szablon aplikacji CLI  
Plik przedstawia profesjonalny układ narzędzia CLI:

- główny parser,
- globalne flagi (`--verbose`, `--token`, …),
- subkomendy (`repos`, `repo`, `invite`),
- osobne funkcje–handlery dla każdej komendy,
- router komend w `main()`,
- kończenie programu z poprawnym kodem wyjścia,
- obsługę błędów i `KeyboardInterrupt`.

Możesz go skopiować do dowolnego projektu i dopisać własną logikę — szkielet jest już gotowy.

📄 Plik: `cli_template.py`  

---

### 2. `Mini Explorer CLI.py` — praktyczny przykład pracy z Path  
Minimalistyczny, ale konkretny program umożliwiający:

- analizę pliku lub katalogu,
- flagi:
  - `--count` — liczba plików,
  - `--list` — lista elementów,
  - `--ext` — filtr rozszerzeń,
  - `--info` — szczegóły pliku,
- walidację błędnych kombinacji flag,
- czytelne komunikaty o błędnym użyciu,
- zwracanie sensownych kodów wyjścia.

Doskonały przykład tego, jak pisać małe, porządne narzędzia developerskie.

📄 Plik: `Mini Explorer CLI.py`  

---

## 🎯 Dlaczego te pliki są wartościowe?

- pokazują świadome projektowanie struktury CLI,
- są gotowymi szablonami,
- świetnie integrują się z testami (`patch`, `Mock`, zwracanie kodów),
- demonstrują realne użycie `pathlib.Path`,
- mają przejrzystą, produkcyjną strukturę.

---

## 🚀 Jak uruchomić przykłady

**CLI Template**
```bash
python cli_template.py --help
python cli_template.py repos Robert
python cli_template.py repo owner_name repo_name
python cli_template.py invite owner repo user
