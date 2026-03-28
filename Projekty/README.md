# Projekty Portfolio

Gotowe i planowane projekty demonstrujące umiejętności praktyczne.
Każdy projekt ma własne README z opisem, instrukcją uruchomienia i strukturą.

---

## Projekty ukończone

### Weather_CLI

Profesjonalny klient API pogodowego. **13/13 testów.**
- requests.Session z timeoutem i walidacją (URL przez `params=`, nagłówek `Accept: application/json`)
- argparse z kodami wyjścia (0/1/2)
- Pełne testy z mockowaniem (pytest + unittest.mock)
- Architektura: separacja klienta (`WeatherClient`) od interfejsu CLI (`main.py`)
- Notatki edukacyjne w `docs/` (WEATHER_CLIENT.md, MAIN.md, TESTY.md)

### Kalkulator

Kalkulator obiektowy z historią operacji. **8/8 testów.**
- Mapowanie operacji przez słownik zamiast łańcucha `if/elif`
- Historia operacji trzymana w liście (pamięć sesji)
- Obsługa błędów: `ZeroDivisionError`, nieznana operacja (`ValueError`), nieprawidłowe dane
- Separacja logiki (`Calculator`) od interakcji z użytkownikiem (`__main__`)
- Type hints, testy jednostkowe pytest

### Mini_Explorer_CLI

Eksplorator systemu plików w terminalu. **7/7 testów.**
- `pathlib` zamiast `os.path` — obiektowa praca ze ścieżkami
- `argparse` z flagami (`--count`, `--list`, `--ext`, `--info`) i aliasami (`-c`, `-l`, `-e`, `-i`)
- Walidacja flag (flagi katalogowe na pliku → kod 2, flagi plikowe na katalogu → kod 2)
- Kody wyjścia zgodne z konwencją Unix (0 sukces / 1 błąd / 2 złe użycie)
- Testy jednostkowe pytest (`tmp_path`, `monkeypatch`, `capsys`)
- Notatki edukacyjne w `docs/` (Mini_Explorer_CLI.md, Testy.md)

### Task_Manager_API

REST API do zarządzania zadaniami. **15/15 testów.**
- FastAPI + SQLAlchemy ORM + PostgreSQL + Pydantic
- Pełne CRUD dla użytkowników, projektów, zadań i tagów
- System tagów (relacja wiele-do-wielu)
- Endpointy statystyk (agregacje SQL — overview, tasks-by-status, tasks-by-priority, user summary)
- Paginacja (offset/limit, Generic `PaginatedResponse[T]`)
- Autoryzacja JWT (bcrypt, OAuth2PasswordBearer, `get_current_user` przez Depends)
  - chronione endpointy z weryfikacją właściciela (owner-only PUT/DELETE)
- Testy pytest + TestClient (SQLite in-memory, StaticPool, fixtures)
- Docker (Dockerfile, docker-compose.yml, `.dockerignore`)
- Notatki edukacyjne w `docs/` (Pydantic, Routery, Paginacja, JWT, Docker)

---

## Projekty ćwiczeniowe

Mniejsze projekty zrealizowane na wcześniejszym etapie nauki.

### Randfacts

Prosty generator losowych ciekawostek.
- Użycie zewnętrznej biblioteki (randfacts)
- Pętla interakcji z użytkownikiem
- Minimalna, ale kompletna aplikacja

---

## Projekty planowane (po ukończeniu mentoringu)

### Neighbors_App

> 📅 **Planowany — po zdobyciu wiedzy z Django i DRF**

Aplikacja webowa do nawiązywania lokalnych kontaktów sąsiedzkich.
Użytkownicy ustawiają aktualny status (np. *„Piwo po pracy"*, *„Spacer z psem"*)
i znajdują osoby w okolicy z podobną potrzebą.

**MVP (znane technologie po mentoringu):**
- Django + Django REST Framework
- PostgreSQL (standardowy)
- System rejestracji i logowania (Django Auth)
- Profile użytkowników z miastem i dzielnicą
- Statusy z kategoriami i filtrowaniem
- Prosty czat (HTTP polling)
- Panel administracyjny (Django Admin)

**Fazy rozwoju (samodzielna nauka):**
- GeoDjango + PostGIS — mapa z lokalizacją
- Docker + docker-compose — konteneryzacja
- Django Channels + Redis — czat w czasie rzeczywistym
- JWT (Simple JWT) — gotowość pod aplikację mobilną
- Celery — zadania w tle (wygaszanie statusów, powiadomienia)
- Deploy na Railway / Fly.io

### AI_Knowledge_Assistant

> 📅 **Planowany — po zdobyciu wiedzy z FastAPI i architektury warstwowej**

Backend RAG (Retrieval-Augmented Generation) — inteligentny asystent odpowiadający na pytania
na podstawie własnej bazy dokumentów. Minimalizuje halucynacje LLM przez wyszukiwanie
relevantnych fragmentów przed wygenerowaniem odpowiedzi.

**Stack technologiczny:**
- FastAPI — framework REST API
- Qdrant — baza wektorowa (open-source, Docker)
- OpenAI API — embeddingi (`text-embedding-3-small`) i LLM (`gpt-4o-mini`)
- LangChain Text Splitters — podział dokumentów na fragmenty (chunking)
- SQLAlchemy — metadane dokumentów i historia zapytań
- Docker + docker-compose — Qdrant + aplikacja w jednym poleceniu
- GitHub Actions — CI (testy, linting)

**Kluczowe funkcje:**
- Upload dokumentów przez API (`.txt`, `.md`, `.pdf`)
- Wyszukiwanie semantyczne (top-k fragmentów)
- Odpowiedź ze wskazaniem źródeł (dokument + fragment + wynik podobieństwa)
- Historia zapytań
- Testy jednostkowe, integracyjne i e2e (min. 70% pokrycia)
