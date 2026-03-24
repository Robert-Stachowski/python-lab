# Task Manager API

## Projekt końcowy - REST API z FastAPI + SQLAlchemy + PostgreSQL

## Opis projektu
System zarządzania zadaniami (Task Manager) zbudowany jako REST API.
Projekt łączy wiedzę z baz danych (SQLAlchemy ORM) z budową backendu (FastAPI).
Zawiera pełne CRUD, statystyki, paginację, autentykację JWT oraz testy pytest.

## Technologie
- **FastAPI** - framework do budowy REST API
- **SQLAlchemy** - ORM do obsługi bazy danych
- **PostgreSQL** - relacyjna baza danych
- **Pydantic[email]** - walidacja danych (schematy request/response)
- **Uvicorn** - serwer ASGI
- **pytest** - testy automatyczne
- **python-jose[cryptography]** - JWT encode/decode
- **passlib[bcrypt]** - hashowanie haseł
- **python-multipart** - obsługa formularzy OAuth2
- **python-dotenv** - zmienne środowiskowe

## Model danych

### User (Użytkownik)
| Kolumna | Typ | Ograniczenia |
|---------|-----|-------------|
| id | Integer | Primary Key |
| username | String(50) | NOT NULL, UNIQUE |
| email | String(100) | NOT NULL, UNIQUE |
| hashed_password | String | NOT NULL |
| is_active | Boolean | default=True |
| created_at | DateTime | default=utcnow |

### Project (Projekt)
| Kolumna | Typ | Ograniczenia |
|---------|-----|-------------|
| id | Integer | Primary Key |
| name | String(100) | NOT NULL |
| description | Text | opcjonalny |
| owner_id | Integer | FK -> User.id |
| created_at | DateTime | default=utcnow |

### Task (Zadanie)
| Kolumna | Typ | Ograniczenia |
|---------|-----|-------------|
| id | Integer | Primary Key |
| title | String(200) | NOT NULL |
| description | Text | opcjonalny |
| status | String(20) | default="todo" (todo/in_progress/done) |
| priority | String(20) | default="medium" (low/medium/high/critical) |
| due_date | Date | opcjonalny |
| created_at | DateTime | default=utcnow |
| updated_at | DateTime | onupdate=utcnow |
| project_id | Integer | FK -> Project.id |
| assignee_id | Integer | FK -> User.id, opcjonalny |

### Tag
| Kolumna | Typ | Ograniczenia |
|---------|-----|-------------|
| id | Integer | Primary Key |
| name | String(50) | NOT NULL, UNIQUE |

### task_tag (Tabela asocjacyjna)
| Kolumna | Typ |
|---------|-----|
| task_id | FK -> Task.id, PK |
| tag_id | FK -> Tag.id, PK |

### Relacje
- User -> Project: 1:N (właściciel projektów)
- User -> Task: 1:N (przypisane zadania)
- Project -> Task: 1:N (cascade delete)
- Task <-> Tag: N:M

## Endpointy API

### Autentykacja
- `POST /auth/register` - rejestracja nowego użytkownika
- `POST /auth/login` - logowanie, zwraca token JWT (pole `username` przyjmuje adres e-mail)

### Users
- `GET /users/me` - dane zalogowanego użytkownika 🔒
- `GET /users` - lista użytkowników (paginacja: skip, limit)
- `GET /users/{id}` - szczegóły użytkownika
- `PUT /users/{id}` - edytuj użytkownika
- `DELETE /users/{id}` - usuń użytkownika

### Projects
- `GET /projects/mine` - projekty zalogowanego użytkownika 🔒
- `GET /projects` - lista projektów (paginacja: skip, limit)
- `POST /projects` - utwórz projekt (owner = zalogowany user) 🔒
- `GET /projects/{id}` - szczegóły projektu (z zadaniami)
- `PUT /projects/{id}` - edytuj projekt
- `DELETE /projects/{id}` - usuń projekt (kaskadowo z zadaniami)

### Tasks
- `GET /tasks` - lista zadań z paginacją i filtrami: status, priority, project_id, assignee_id
- `POST /tasks` - utwórz zadanie (brak autoryzacji — endpoint publiczny)
- `GET /tasks/{id}` - szczegóły zadania
- `PUT /tasks/{id}` - edytuj zadanie
- `PATCH /tasks/{id}/status` - zmień status zadania
- `DELETE /tasks/{id}` - usuń zadanie

### Tags
- `GET /tags` - lista tagów (paginacja: skip, limit)
- `POST /tags` - utwórz tag
- `POST /tasks/{id}/tags` - dodaj tag do zadania
- `DELETE /tasks/{id}/tags/{tag_id}` - usuń tag z zadania

### Statystyki
- `GET /stats/overview` - ogólne statystyki (liczba zadań, projektów, użytkowników)
- `GET /stats/tasks-by-status` - zadania pogrupowane po statusie
- `GET /stats/tasks-by-priority` - zadania pogrupowane po priorytecie
- `GET /stats/user/{id}/summary` - podsumowanie użytkownika

> 🔒 — endpoint wymaga tokena JWT w headerze: `Authorization: Bearer <token>`

## Paginacja

Endpointy listujące zasoby obsługują paginację przez parametry query:
- `skip` — ile rekordów pominąć (domyślnie: 0)
- `limit` — ile rekordów zwrócić (domyślnie: 10, max: 100)

Przykład: `GET /tasks?skip=0&limit=20&status=todo`

Format odpowiedzi:
```json
{
  "total": 42,
  "skip": 0,
  "limit": 20,
  "items": [...]
}
```

## Struktura projektu

```
Task_Manager_API/
├── README.md
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── app/
│   ├── __init__.py
│   ├── main.py              # Punkt wejścia FastAPI
│   ├── config.py            # Konfiguracja JWT (SECRET_KEY, ALGORITHM)
│   ├── database.py          # Połączenie z bazą danych
│   ├── models.py            # Modele SQLAlchemy
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── hashing.py       # Hashowanie haseł (bcrypt)
│   │   ├── jwt.py           # Tworzenie i weryfikacja tokenów JWT
│   │   └── dependencies.py  # get_current_user() — Depends()
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py          # Schematy Pydantic dla User
│   │   ├── project.py       # Schematy dla Project
│   │   ├── task.py          # Schematy dla Task
│   │   ├── tag.py           # Schematy dla Tag
│   │   ├── auth.py          # Token, TokenData
│   │   └── pagination.py    # PaginatedResponse[T]
│   └── routers/
│       ├── __init__.py
│       ├── auth.py          # Endpointy autentykacji
│       ├── users.py         # Endpointy User
│       ├── projects.py      # Endpointy Project
│       ├── tasks.py         # Endpointy Task
│       ├── tags.py          # Endpointy Tag
│       └── stats.py         # Endpointy statystyk
└── tests/
    ├── __init__.py
    ├── conftest.py          # Konfiguracja testów (SQLite in-memory)
    ├── test_users.py
    ├── test_projects.py
    └── test_tasks.py
```

## Wymagania

### Opcja A: Docker (zalecana)
- [Docker Desktop](https://www.docker.com/products/docker-desktop)

### Opcja B: lokalnie
- Python 3.12+
- PostgreSQL 15+

---

## Jak uruchomić

### Opcja A: Docker (zalecana)

```bash
# Skonfiguruj .env (SECRET_KEY wymagany)
cp .env.example .env

# Uruchom aplikację + bazę danych
docker-compose up --build
```

Aplikacja dostępna na `http://localhost:8000/docs`

### Opcja B: lokalnie

### 1. Zainstaluj zależności
```bash
pip install -r requirements.txt
```

> **Uwaga dla Windows:** jeśli wystąpi błąd z `bcrypt`, zainstaluj starszą wersję: `pip install bcrypt==3.2.2`

### 2. Skonfiguruj zmienne środowiskowe
```bash
cp .env.example .env
# Edytuj .env i ustaw:
# DATABASE_URL=postgresql://user:password@localhost/dbname
# SECRET_KEY=twoj-bardzo-tajny-klucz-minimum-32-znaki
```

### 3. Uruchom serwer
```bash
python -m uvicorn app.main:app --reload
```

### 4. Otwórz dokumentację API
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 5. Uruchom testy
```bash
# Windows (Git CMD / PowerShell)
.venv\Scripts\python.exe -m pytest tests/ -v

# Linux / Mac
pytest tests/ -v
```

## Co zostało zrealizowane

### Etap 1: Modele i baza danych
- [x] Modele SQLAlchemy w `app/models.py`
- [x] Konfiguracja połączenia z bazą w `app/database.py`
- [x] Automatyczne tworzenie tabel przy starcie aplikacji

### Etap 2: Schematy Pydantic
- [x] Schematy request/response w `app/schemas/`
- [x] Trzy schematy na model: Create, Update, Response

### Etap 3: Endpointy CRUD
- [x] Pełne CRUD dla Users
- [x] Pełne CRUD dla Projects
- [x] Pełne CRUD dla Tasks (z filtrami: status, priority, project_id, assignee_id)
- [x] Endpointy dla Tags (tworzenie, przypisywanie do zadań, usuwanie)

### Etap 4: Statystyki
- [x] Endpointy statystyk w `app/routers/stats.py`
- [x] Agregacje SQL: COUNT, GROUP BY (overview, by-status, by-priority, user summary)

### Etap 5: Testy
- [x] 15/15 testów przechodzi
- [x] TestClient z FastAPI + SQLite in-memory jako baza testowa
- [x] Fixtures w `conftest.py`, dependency_overrides dla izolacji testów

### Etap 6 (Bonus): Rozszerzenia
- [x] Autentykacja JWT (rejestracja, logowanie, chronione endpointy)
- [x] Paginacja dla endpointów listujących (PaginatedResponse[T], skip/limit)
- [x] Dockerfile + docker-compose.yml z PostgreSQL
