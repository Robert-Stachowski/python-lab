# Python -> Django: Moja sciezka nauki

Repozytorium dokumentujace moja droge od podstaw Pythona do web developmentu w Django.
Sluzy jako osobista sciaga, zestaw cwiczen i portfolio projektow.

## Mapa umiejetnosci

- [x] Zmienne, typy danych, petle, warunki
- [x] Slicing i comprehension (list, dict, set)
- [x] Funkcje (def, lambda, map, filter, reduce, any, all, zip)
- [x] Programowanie obiektowe (klasy, dziedziczenie, enkapsulacja, polimorfizm)
- [x] Obsluga wyjatkow (try/except/else/finally/raise)
- [x] Obsluga plikow (TXT, JSON)
- [x] Moduly (wbudowane i zewnetrzne)
- [x] Testowanie (unittest, pytest, mock)
- [x] SQLAlchemy ORM (sesje, modele, filtrowanie, JOINy, relacje)
- [ ] Django (w trakcie)
- [ ] Django REST Framework
- [ ] Deploy

## Struktura repozytorium

```
Podstawy_Pythona/    - zmienne, typy danych, slicing, comprehension, dobre praktyki
Funkcje/             - funkcje, lambda, map/filter/reduce, sum/any/all
OOP/                 - klasy, dziedziczenie, polimorfizm, abstrakcja
Wyjatki/             - try/except/else/finally/raise
Pliki_i_JSON/        - obsluga plikow TXT i JSON, cwiczenia praktyczne
Moduly/              - moduly wbudowane, zewnetrzne, tworzenie wlasnych
Testowanie/          - unittest, pytest, mock, fixtures, parametrize
SQLAlchemy/          - ORM, sesje, modele, filtrowanie, JOINy, agregacje
Projekty/            - gotowe projekty portfolio
Szablony/            - szablony do ponownego uzycia (CLI, itp.)
Django/              - nastepny etap nauki (w przygotowaniu)
```

## Projekty portfolio

| Projekt | Opis | Czego uczy |
|---------|------|------------|
| [Weather_CLI](Projekty/Weather_CLI/) | Klient API pogodowego z testami | requests, argparse, mock, architektura |
| [Kalkulator](Projekty/Kalkulator/) | Kalkulator OOP z historia operacji | klasy, SRP, mapowanie operacji |
| [Mini Explorer CLI](Projekty/Mini_Explorer_CLI/) | Eksplorator systemu plikow | pathlib, argparse, flagi |
| [Randfacts](Projekty/Randfacts/) | Generator losowych faktow | pip, biblioteki zewnetrzne |

## Jak uruchomic

```bash
# klonowanie
git clone <url-repo>
cd First_step_by_Python_code

# instalacja zaleznosci
pip install -r requirements.txt

# uruchomienie dowolnego skryptu
python Podstawy_Pythona/hello.py
python Projekty/Weather_CLI/main.py --city Warszawa

# testy
pytest Testowanie/pytest_przyklady/
pytest Projekty/Weather_CLI/tests/
```

## Autor

Robert Stachowski - Python/Django Web Developer w trakcie nauki
GitHub: https://github.com/Robert-Stachowski
