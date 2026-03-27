# Python -> Django: Moja ścieżka nauki

Repozytorium dokumentujące moją drogę od podstaw Pythona do web developmentu w Django.
Służy jako osobista ściąga, zestaw ćwiczeń i portfolio projektów.

## Mapa umiejętności

- [x] Zmienne, typy danych, pętle, warunki
- [x] Slicing i comprehension (list, dict, set)
- [x] Funkcje (def, lambda, map, filter, reduce, any, all, zip)
- [x] Programowanie obiektowe (klasy, dziedziczenie, enkapsulacja, polimorfizm)
- [x] Obsługa wyjątków (try/except/else/finally/raise)
- [x] Obsługa plików (TXT, JSON)
- [x] Moduły (wbudowane i zewnętrzne)
- [x] Testowanie (unittest, pytest, mock)
- [x] SQLAlchemy ORM (sesje, modele, filtrowanie, JOINy, relacje)
- [x] Bazy danych - ćwiczenia praktyczne (SQLite + PostgreSQL)
- [x] FastAPI + SQLAlchemy (REST API, JWT, paginacja, Docker, testy)
- [ ] Django (w trakcie)
- [ ] Django REST Framework
- [ ] Deploy

## Struktura repozytorium

```
Podstawy_Pythona/    - zmienne, typy danych, slicing, comprehension, dobre praktyki
Funkcje/             - funkcje, lambda, map/filter/reduce, sum/any/all
OOP/                 - klasy, dziedziczenie, polimorfizm, abstrakcja
Wyjatki/             - try/except/else/finally/raise
Pliki_i_JSON/        - obsługa plików TXT i JSON, ćwiczenia praktyczne
Moduly/              - moduły wbudowane, zewnętrzne, tworzenie własnych
Testowanie/          - unittest, pytest, mock, fixtures, parametrize
SQLAlchemy/          - ORM, sesje, modele, filtrowanie, JOINy, agregacje
Bazy_danych/         - 10 ćwiczeń praktycznych (CRUD, relacje, agregacje, subquery)
Projekty/            - gotowe projekty portfolio
Szablony/            - szablony do ponownego użycia (CLI, itp.)
Django/              - następny etap nauki (w przygotowaniu)
```

## Projekty portfolio

| Projekt | Opis | Czego uczy | Testy |
|---------|------|------------|-------|
| [Weather_CLI](Projekty/Weather_CLI/) | Klient API pogodowego — architektura CLI z requester pattern, obsługa błędów, kody wyjścia | requests.Session, argparse, unittest.mock, separation of concerns | 13/13 |
| [Kalkulator](Projekty/Kalkulator/) | Kalkulator OOP — mapowanie operacji przez słownik, historia sesji, type hints | klasy, SRP, obsługa wyjątków, pytest | 8/8 |
| [Task Manager API](Projekty/Task_Manager_API/) | REST API do zarządzania zadaniami — pełny backend z autentykacją i Dockerem | FastAPI, SQLAlchemy, PostgreSQL, Pydantic, JWT, Docker, pytest | 15/15 |
| [Mini Explorer CLI](Projekty/Mini_Explorer_CLI/) | Eksplorator systemu plików w terminalu | pathlib, argparse, flagi | — |
| [Randfacts](Projekty/Randfacts/) | Generator losowych faktów | pip, biblioteki zewnętrzne | — |
| [Neighbors App](Projekty/Neighbors_App/) | Aplikacja do lokalnych spotkań sąsiedzkich *(planowana)* | Django, DRF, PostgreSQL, GeoDjango | — |
| [AI Knowledge Assistant](Projekty/AI_Knowledge_Assistant/) | RAG backend — asystent z własną bazą wiedzy *(planowany)* | FastAPI, OpenAI, Qdrant, embeddings, LangChain | — |

## Jak uruchomić

```bash
# klonowanie
git clone <url-repo>
cd python-lab

# instalacja zależności (każdy projekt ma własny requirements.txt)
pip install -r Projekty/Task_Manager_API/requirements.txt

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
