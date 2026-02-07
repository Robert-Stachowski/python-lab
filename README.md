# Python -> Django: Moja ścieżka nauki

Repozytorium dokumentujące moją drogę od podstaw Pythona do web developmentu w Django.
Służy jako osobista ściąga, zestaw ćwiczeń i portfolio projektów.

## Mapa umiejętności

- [x] Zmienne, typy danych, pętle, warunki
- [x] Slicing i comprehension (list, dict, set)
- [x] Funkcje (def, lambda, map, filter, reduce, any, all, zip)
- [x] Programowanie obiektowe (klasy, dziedziczenie, enkapsulacja, polimorfizm)
- [x] Obsługa wyjątkow (try/except/else/finally/raise)
- [x] Obsługa plikow (TXT, JSON)
- [x] Moduły (wbudowane i zewnętrzne)
- [x] Testowanie (unittest, pytest, mock)
- [x] SQLAlchemy ORM (sesje, modele, filtrowanie, JOINy, relacje)
- [ ] Bazy danych - cwiczenia praktyczne (SQLite + PostgreSQL)
- [ ] FastAPI + SQLAlchemy (REST API)
- [ ] Django (w trakcie)
- [ ] Django REST Framework
- [ ] Deploy

## Struktura repozytorium

```
Podstawy_Pythona/    - zmienne, typy danych, slicing, comprehension, dobre praktyki
Funkcje/             - funkcje, lambda, map/filter/reduce, sum/any/all
OOP/                 - klasy, dziedziczenie, polimorfizm, abstrakcja
Wyjatki/             - try/except/else/finally/raise
Pliki_i_JSON/        - obsługa plikow TXT i JSON, cwiczenia praktyczne
Moduly/              - moduły wbudowane, zewnetrzne, tworzenie własnych
Testowanie/          - unittest, pytest, mock, fixtures, parametrize
SQLAlchemy/          - ORM, sesje, modele, filtrowanie, JOINy, agregacje
Bazy_danych/         - 10 cwiczen praktycznych (CRUD, relacje, agregacje, subquery)
Projekty/            - gotowe projekty portfolio
Szablony/            - szablony do ponownego uzycia (CLI, itp.)
Django/              - nastepny etap nauki (w przygotowaniu)
```

## Projekty portfolio

| Projekt | Opis | Czego uczy |
|---------|------|------------|
| [Weather_CLI](Projekty/Weather_CLI/) | Klient API pogodowego z testami | requests, argparse, mock, architektura |
| [Kalkulator](Projekty/Kalkulator/) | Kalkulator OOP z historią operacji | klasy, SRP, mapowanie operacji |
| [Mini Explorer CLI](Projekty/Mini_Explorer_CLI/) | Eksplorator systemu plikow | pathlib, argparse, flagi |
| [Randfacts](Projekty/Randfacts/) | Generator losowych faktow | pip, biblioteki zewnętrzne |
| [Task Manager API](Projekty/Task_Manager_API/) | REST API do zarzadzania zadaniami | FastAPI, SQLAlchemy, PostgreSQL, Pydantic |

## Jak uruchomić

```bash
# klonowanie
git clone <url-repo>
cd First_step_by_Python_code

# instalacja zależności
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
