# Task Manager API

## Projekt koncowy - REST API z FastAPI + SQLAlchemy + PostgreSQL

## Opis projektu
System zarzadzania zadaniami (Task Manager) zbudowany jako REST API.
Projekt laczy wiedze z baz danych (SQLAlchemy ORM) z budowa backendu (FastAPI).

## Technologie
- **FastAPI** - framework do budowy REST API
- **SQLAlchemy** - ORM do obslugi bazy danych
- **PostgreSQL** - relacyjna baza danych
- **Pydantic** - walidacja danych (schematy request/response)
- **Uvicorn** - serwer ASGI
- **pytest** - testy

## Model danych

### User (Uzytkownik)
| Kolumna | Typ | Ograniczenia |
|---------|-----|-------------|
| id | Integer | Primary Key |
| username | String(50) | NOT NULL, UNIQUE |
| email | String(100) | NOT NULL, UNIQUE |
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
- User -> Project: 1:N (wlasciciel projektow)
- User -> Task: 1:N (przypisane zadania)
- Project -> Task: 1:N (cascade delete)
- Task <-> Tag: N:M

## Endpointy API

### Users
- `GET /users` - lista uzytkownikow
- `POST /users` - utworz uzytkownika
- `GET /users/{id}` - szczegoly uzytkownika
- `PUT /users/{id}` - edytuj uzytkownika
- `DELETE /users/{id}` - usun uzytkownika

### Projects
- `GET /projects` - lista projektow
- `POST /projects` - utworz projekt
- `GET /projects/{id}` - szczegoly projektu (z zadaniami)
- `PUT /projects/{id}` - edytuj projekt
- `DELETE /projects/{id}` - usun projekt (kaskadowo z zadaniami)

### Tasks
- `GET /tasks` - lista zadan (z filtrami: status, priority, project_id, assignee_id)
- `POST /tasks` - utworz zadanie
- `GET /tasks/{id}` - szczegoly zadania
- `PUT /tasks/{id}` - edytuj zadanie
- `PATCH /tasks/{id}/status` - zmien status zadania
- `DELETE /tasks/{id}` - usun zadanie

### Tags
- `GET /tags` - lista tagow
- `POST /tags` - utworz tag
- `POST /tasks/{id}/tags` - dodaj tag do zadania
- `DELETE /tasks/{id}/tags/{tag_id}` - usun tag z zadania

### Statystyki
- `GET /stats/overview` - ogolne statystyki (liczba zadan, projektow, uzytkownikow)
- `GET /stats/tasks-by-status` - zadania pogrupowane po statusie
- `GET /stats/tasks-by-priority` - zadania pogrupowane po priorytecie
- `GET /stats/user/{id}/summary` - podsumowanie uzytkownika

## Struktura projektu

```
Task_Manager_API/
├── README.md
├── requirements.txt
├── .env.example
├── app/
│   ├── __init__.py
│   ├── main.py              # Punkt wejscia FastAPI
│   ├── database.py           # Polaczenie z baza danych
│   ├── models.py             # Modele SQLAlchemy
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py           # Schematy Pydantic dla User
│   │   ├── project.py        # Schematy dla Project
│   │   ├── task.py           # Schematy dla Task
│   │   └── tag.py            # Schematy dla Tag
│   └── routers/
│       ├── __init__.py
│       ├── users.py          # Endpointy User
│       ├── projects.py       # Endpointy Project
│       ├── tasks.py          # Endpointy Task
│       ├── tags.py           # Endpointy Tag
│       └── stats.py          # Endpointy statystyk
└── tests/
    ├── __init__.py
    ├── conftest.py           # Konfiguracja testow
    ├── test_users.py
    ├── test_projects.py
    └── test_tasks.py
```

## Jak uruchomic

### 1. Zainstaluj zaleznosci
```bash
pip install -r requirements.txt
```

### 2. Skonfiguruj baze danych
```bash
cp .env.example .env
# Edytuj .env i ustaw DATABASE_URL
```

### 3. Uruchom serwer
```bash
uvicorn app.main:app --reload
```

### 4. Otworz dokumentacje API
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 5. Uruchom testy
```bash
pytest tests/ -v
```

## Zadania do zrealizowania

### Etap 1: Modele i baza danych
- [ ] Zdefiniuj modele w `app/models.py`
- [ ] Skonfiguruj polaczenie w `app/database.py`
- [ ] Przetestuj tworzenie tabel

### Etap 2: Schematy Pydantic
- [ ] Utworz schematy request/response w `app/schemas/`
- [ ] Pamietaj o schematach: Create, Update, Response

### Etap 3: Endpointy CRUD
- [ ] Zaimplementuj CRUD dla Users
- [ ] Zaimplementuj CRUD dla Projects
- [ ] Zaimplementuj CRUD dla Tasks (z filtrami)
- [ ] Zaimplementuj endpointy dla Tags

### Etap 4: Statystyki
- [ ] Zaimplementuj endpointy statystyk
- [ ] Uzyj agregacji SQL (COUNT, AVG, GROUP BY)

### Etap 5: Testy
- [ ] Napisz testy dla endpointow
- [ ] Uzyj TestClient z FastAPI

### Etap 6 (Bonus): Rozszerzenia
- [ ] Dodaj autentykacje (JWT)
- [ ] Dodaj paginacje do list
- [ ] Dodaj Dockerfile
- [ ] Dodaj docker-compose.yml z PostgreSQL
