# Ściągawka: Routery w FastAPI

## Po co w ogóle routery?

FastAPI to framework do budowania REST API. Twój serwer **czeka na requesty HTTP** — ktoś wysyła żądanie i serwer odpowiada.

Każdy request ma:
- **Adres (URL)** — do czego się odwołujesz: `/users`, `/tasks`, `/projects`
- **Metodę** — co chcesz zrobić: GET (pobierz), POST (stwórz), PUT (zmień), DELETE (usuń)
- **Dane** (opcjonalnie) — co przekazujesz w body: `{"username": "Jan", "email": "jan@x.com"}`

**Router** to plik który zbiera wszystkie endpointy (adresy URL) dla jednego zasobu.
Bez routerów wszystko byłoby w jednym pliku `main.py` — chaos przy 20+ endpointach.

```
routers/
  users.py     ← wszystko co dotyczy /users
  projects.py  ← wszystko co dotyczy /projects
  tasks.py     ← wszystko co dotyczy /tasks
  tags.py      ← wszystko co dotyczy /tags
```

---

## Miejsce routerów w architekturze

```
HTTP Request
     ↓
main.py          ← punkt wejścia, kieruje ruch do odpowiednich routerów
     ↓
routers/         ← logika endpointu: walidacja, obsługa błędów, zapis/odczyt
     ↓
schemas/         ← Pydantic: walidacja danych wejściowych i serializacja odpowiedzi
     ↓
models.py        ← SQLAlchemy: zapis i odczyt z bazy
     ↓
PostgreSQL
```

---

## Dekorator — co to jest `@`?

Dekorator to funkcja która **opakowuje inną funkcję** i dodaje jej nowe zachowanie.

```python
@router.get("/")
def get_users():
    return []
```

`@router.get("/")` mówi FastAPI: *"kiedy przyjdzie GET na `/`, uruchom funkcję `get_users`"*.

Bez dekoratora `get_users` jest zwykłą funkcją Pythona — FastAPI nic o niej nie wie.

Dekorator w FastAPI robi trzy rzeczy naraz:
- rejestruje URL i metodę HTTP
- ustawia `response_model` i `status_code`
- podpina walidację Pydantic

---

## Podłączenie routera w main.py

Router sam w sobie nic nie robi — musisz go zarejestrować w aplikacji:

```python
# main.py
from fastapi import FastAPI
from .routers import users, projects, tasks, tags

app = FastAPI()

app.include_router(users.router,    prefix="/users",    tags=["Users"])
app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(tasks.router,    prefix="/tasks",    tags=["Tasks"])
app.include_router(tags.router,     prefix="/tags",     tags=["Tags"])
```

- `prefix="/users"` → każdy endpoint w `users.py` dostaje przedrostek `/users`
  - `@router.get("/")` staje się `GET /users/`
  - `@router.get("/{user_id}")` staje się `GET /users/{user_id}`
- `tags=["Users"]` → grupuje endpointy w Swagger UI pod adresem `/docs`

---

## Depends(get_db) — skąd się bierze sesja bazy?

Do bazy potrzebne jest **połączenie (sesja)**. Nie tworzysz go sam — FastAPI robi to za Ciebie.

```python
# database.py
def get_db():
    db = SessionLocal()   # otwórz połączenie
    try:
        yield db          # przekaż do endpointu
    finally:
        db.close()        # zamknij po zakończeniu requestu
```

`Depends(get_db)` w argumencie funkcji mówi FastAPI:
*"zanim uruchomisz moją funkcję, wywołaj `get_db()` i wstrzyknij wynik jako `db`"*

```python
def get_users(db: Session = Depends(get_db)):
    #                        ↑ FastAPI wywołuje get_db() i podaje wynik tutaj
```

Ty piszesz tylko `db.query(...)` — otwieranie i zamykanie połączenia dzieje się automatycznie.

---

## Metody HTTP i ich znaczenie

| Dekorator | Metoda HTTP | Kiedy używany | Status |
|---|---|---|---|
| `@router.get("/")` | GET | Pobierz listę | 200 |
| `@router.get("/{id}")` | GET | Pobierz jeden rekord | 200 |
| `@router.post("/")` | POST | Utwórz nowy rekord | **201** |
| `@router.put("/{id}")` | PUT | Aktualizuj rekord | 200 |
| `@router.patch("/{id}/status")` | PATCH | Zmień jedno pole | 200 |
| `@router.delete("/{id}")` | DELETE | Usuń rekord | **204** |

---

## Pięć etapów CRUD — krok po kroku

### Etap 1 — GET `/` — lista wszystkich

```python
@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()   # SELECT * FROM users
```

Najprostszy endpoint. Zapytaj bazę, zwróć wynik.

---

### Etap 2 — POST `/` — tworzenie rekordu

```python
@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```

**`user: UserCreate`** — Pydantic automatycznie waliduje JSON z body requestu.
Jeśli dane są niepoprawne → **422 automatycznie**, funkcja się nie wykonuje.

**`user.model_dump()`** — zamienia obiekt Pydantic na słownik:
```python
{"username": "Jan", "email": "jan@x.com"}
```

**`**user.model_dump()`** — rozpakowuje słownik jako argumenty, równoważne z:
```python
models.User(username="Jan", email="jan@x.com")
```

**`db.add()` → `db.commit()` → `db.refresh()`**:
```python
db.add(db_user)      # dodaj do kolejki zapisu
db.commit()          # wyślij INSERT do bazy — baza nadaje id i created_at
db.refresh(db_user)  # pobierz z bazy wygenerowane wartości (id, created_at)
```

---

### Etap 3 — GET `/{user_id}` — pobieranie jednego rekordu

```python
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

**`/{user_id}`** — FastAPI wyciąga wartość z URL automatycznie.
`GET /users/42` → `user_id = 42`

**`.filter(...).first()`** — odpowiednik `WHERE id = 42 LIMIT 1`.
Zwraca obiekt albo `None` jeśli nie znalazł.

**`HTTPException`** — jeśli rekord nie istnieje, rzuć błąd:
```python
raise HTTPException(status_code=404, detail="User not found")
# klient dostaje: 404  {"detail": "User not found"}
```

---

### Etap 4 — PUT `/{user_id}` — aktualizacja rekordu

```python
@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    return db_user
```

**`exclude_unset=True`** — klient wysłał tylko `{"username": "Janek"}`.
Bez tego `model_dump()` zwróciłby `{"username": "Janek", "email": None, "is_active": None}`
i nadpisałbyś pola których klient nie chciał zmieniać.
Z `exclude_unset=True` → `{"username": "Janek"}` — tylko to co faktycznie przyszło.

**`setattr(db_user, field, value)`** — dynamiczne ustawienie atrybutu obiektu:
```python
setattr(db_user, "username", "Janek")
# to samo co: db_user.username = "Janek"
```
Potrzebne bo nie wiesz z góry które pola klient zmienił — pętla obsługuje każdą kombinację.

Brak `db.add()` — obiekt już jest w bazie, SQLAlchemy śledzi zmiany automatycznie.

---

### Etap 5 — DELETE `/{user_id}` — usuwanie rekordu

```python
@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
```

**`status_code=204`** — 204 No Content: operacja udana, brak treści do zwrócenia.
Dlatego brak `return` i brak `response_model`.

---

### Etap 6 — Query parametry, czyli filtry w URL

Zamiast pobierać wszystkie rekordy naraz, klient może filtrować przez URL:

```
GET /tasks?status=todo
GET /tasks?status=todo&project_id=3
GET /tasks?priority=high
```

```python
from fastapi import Query
from typing import Optional

@router.get("/", response_model=list[TaskResponse])
def get_tasks(
    status: Optional[str] = Query(None, description="Filtruj po statusie"),
    priority: Optional[str] = Query(None, description="Filtruj po priorytecie"),
    project_id: Optional[int] = Query(None, description="Filtruj po projekcie"),
    db: Session = Depends(get_db),
):
```

Każdy query parametr to argument funkcji z domyślną wartością `None` — czyli opcjonalny.
Jeśli klient go nie wyśle, zmienna ma wartość `None`.

**Dynamiczne budowanie zapytania** — nie wiesz z góry które filtry przyjdą:

```python
query = db.query(models.Task)                # zacznij od SELECT * FROM tasks

if status is not None:
    query = query.filter(models.Task.status == status)      # dodaj WHERE status = ...

if priority is not None:
    query = query.filter(models.Task.priority == priority)  # dodaj AND priority = ...

if project_id is not None:
    query = query.filter(models.Task.project_id == project_id)

return query.all()   # dopiero teraz wykonaj zapytanie
```

Zapytanie SQL buduje się tylko z tych filtrów które faktycznie przyszły.

---

### Etap 7 — PATCH, czyli zmiana jednego pola

PUT zmienia cały rekord. PATCH zmienia **jedno konkretne pole** — np. tylko status zadania:

```python
@router.patch("/{task_id}/status", response_model=TaskResponse)
def update_task_status(task_id: int, status_update: TaskStatusUpdate, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = status_update.status   # bezpośrednie przypisanie — tylko jedno pole

    db.commit()
    db.refresh(task)
    return task
```

Schemat `TaskStatusUpdate` ma tylko jedno pole — dlatego zamiast pętli `for` wystarczy
proste przypisanie.

| | PUT | PATCH |
|---|---|---|
| Co zmienia | cały rekord | jedno konkretne pole |
| Schemat | `XxxUpdate` (wszystko Optional) | np. `TaskStatusUpdate` (tylko status) |
| Zapis | pętla `for` + `setattr` | bezpośrednie przypisanie |
| URL | `/{id}` | `/{id}/status` |

---

### Etap 8 — relacje przy pobieraniu (task z tagami)

Gdy pobierasz `Task` z bazy, SQLAlchemy domyślnie **nie ładuje tagów** — to osobna tabela.
Jeśli `TaskResponse` ma pole `tags: List[TagResponse]`, a tagi nie są załadowane — dostaniesz pustą listę.

Rozwiązanie — `selectinload`:

```python
from sqlalchemy.orm import selectinload

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = (
        db.query(models.Task)
        .options(selectinload(models.Task.tags))   # załaduj też tagi jednym zapytaniem
        .filter(models.Task.id == task_id)
        .first()
    )
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
```

`selectinload` mówi SQLAlchemy: *"przy pobieraniu taska zrób też zapytanie po tagi i dołącz je"*.

Używaj `selectinload` tylko gdy schemat Response zawiera zagnieżdżone obiekty:
```python
tags: List[TagResponse] = []     # ← potrzebujesz selectinload
tasks: List[TaskResponse] = []   # ← i tutaj też
```

---

### Etap 9 — dodatkowa walidacja w endpoincie

Pydantic sprawdza typy i format. Nie sprawdzi czy `project_id` który podałeś **naprawdę istnieje w bazie** — to musisz zrobić sam:

```python
@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):

    # Sprawdź czy projekt istnieje
    project = db.query(models.Project).filter(models.Project.id == task.project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    # Sprawdź czy assignee istnieje (jeśli podano)
    if task.assignee_id is not None:
        user = db.query(models.User).filter(models.User.id == task.assignee_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="Assignee not found")

    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task
```

**Zasada:** Pydantic sprawdza format danych, Ty sprawdzasz istnienie rekordów w bazie.

---

## Podsumowanie CRUD

| Endpoint | Metoda | Status | Schemat wejścia | Schemat wyjścia |
|---|---|---|---|---|
| `GET /users/` | GET | 200 | — | `list[UserResponse]` |
| `POST /users/` | POST | 201 | `UserCreate` | `UserResponse` |
| `GET /users/{id}` | GET | 200 | — | `UserResponse` |
| `PUT /users/{id}` | PUT | 200 | `UserUpdate` | `UserResponse` |
| `PATCH /tasks/{id}/status` | PATCH | 200 | `TaskStatusUpdate` | `TaskResponse` |
| `DELETE /users/{id}` | DELETE | 204 | — | — |

---

### Etap 10 — sprawdzanie duplikatów

Pydantic sprawdza format, ale nie sprawdzi czy email już istnieje w bazie.
Sprawdzasz sam, **zanim** zapiszesz:

```python
@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    existing = db.query(models.User).filter(models.User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")

    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```

- **400** — dane poprawne formatowo, ale logicznie niedopuszczalne (duplikat)
- **404** — rekord nie istnieje
- **422** — zły format danych (automatyczny, Pydantic)

---

### Etap 11 — relacje N:M w routerze (dodawanie tagów do taska)

Nowy wzorzec — nie tworzysz nowego rekordu, tylko **łączysz dwa istniejące**.
Task i Tag istnieją osobno. Przypisanie tagu do taska = dodanie wiersza do tabeli `task_tag`.

```python
# POST /tags/tasks/{task_id}/tags
@router.post("/tasks/{task_id}/tags", status_code=201)
def add_tag_to_task(task_id: int, tag: TagCreate, db: Session = Depends(get_db)):

    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    # Znajdź tag lub utwórz nowy jeśli nie istnieje
    db_tag = db.query(models.Tag).filter(models.Tag.name == tag.name).first()
    if db_tag is None:
        db_tag = models.Tag(name=tag.name)
        db.add(db_tag)
        db.flush()   # zapisz do bazy bez commita — potrzebujemy id taga

    if db_tag in task.tags:
        raise HTTPException(status_code=400, detail="Tag already assigned to this task")

    task.tags.append(db_tag)   # SQLAlchemy samo doda wiersz do task_tag
    db.commit()
```

Kluczowe: `task.tags.append(db_tag)` — nie piszesz ręcznie `INSERT INTO task_tag`.
SQLAlchemy widzi że dodałeś do listy i samo obsługuje tabelę pośrednią.

`db.flush()` — zapisuje do bazy ale **nie commituje**. Używasz gdy potrzebujesz id nowego rekordu przed zakończeniem transakcji.

Usuwanie tagu działa odwrotnie:

```python
# DELETE /tags/tasks/{task_id}/tags/{tag_id}
@router.delete("/tasks/{task_id}/tags/{tag_id}", status_code=204)
def remove_tag_from_task(task_id: int, tag_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")

    if tag not in task.tags:
        raise HTTPException(status_code=400, detail="Tag not assigned to this task")

    task.tags.remove(tag)   # SQLAlchemy samo usunie wiersz z task_tag
    db.commit()
```

---

### Etap 12 — pełny blok importów w routerze

Każdy plik routera zaczyna się od tych samych importów:

```python
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, selectinload
from typing import Optional

from ..database import get_db       # .. oznacza katalog wyżej (app/)
from .. import models               # modele SQLAlchemy
from ..schemas import (             # schematy Pydantic
    UserCreate,
    UserUpdate,
    UserResponse,
)

router = APIRouter()
```

`..` — routery są w `app/routers/`, więc `..` to `app/`.
Importujesz tylko to czego używasz w danym pliku.

---

## Pełny obraz — co może robić plik routera

| Operacja | Kod | Kiedy |
|---|---|---|
| Pobierz wszystkie | `db.query(...).all()` | GET `/` |
| Pobierz jeden | `db.query(...).filter(...).first()` | GET `/{id}` |
| Filtruj | `.filter(...).filter(...)` | Query parametry |
| Załaduj relacje | `.options(selectinload(...))` | gdy Response ma zagnieżdżone obiekty |
| Utwórz | `db.add()` + `db.commit()` | POST |
| Zaktualizuj | `setattr()` + `db.commit()` | PUT / PATCH |
| Usuń | `db.delete()` + `db.commit()` | DELETE |
| Dodaj do N:M | `lista.append()` + `db.commit()` | POST relacja |
| Usuń z N:M | `lista.remove()` + `db.commit()` | DELETE relacja |
| Zapisz bez commita | `db.flush()` | gdy potrzebujesz id przed commitem |
| Błąd nie znaleziono | `HTTPException(404)` | rekord nie istnieje |
| Błąd logiczny | `HTTPException(400)` | duplikat, zła kombinacja |
| Błąd formatu | automatyczny 422 | Pydantic walidacja |

---

## Jak response_model działa przy zwracaniu

`return db_user` zawsze zwraca **obiekt SQLAlchemy**. To `response_model` w dekoratorze
decyduje jak Pydantic go przetworzy przed wysłaniem do klienta:

```
baza → obiekt SQLAlchemy → [response_model=UserResponse] → JSON → klient
```

`from_attributes = True` w schemacie Response pozwala Pydanticowi czytać atrybuty
obiektu SQLAlchemy zamiast słownika. Bez tego dostałbyś błąd.

---

## Kody HTTP — szybka ściąga

| Kod | Znaczenie | Kiedy |
|---|---|---|
| 200 | OK | domyślny, wszystko OK |
| 201 | Created | po udanym POST |
| 204 | No Content | po udanym DELETE |
| 400 | Bad Request | nieprawidłowe dane (np. email już zajęty) |
| 404 | Not Found | rekord nie istnieje w bazie |
| 422 | Unprocessable Entity | błąd walidacji Pydantic (automatyczny) |

---

## Zasady zwracania danych — złota zasada REST API

**Wszystko co wychodzi z serwera → JSON. Wszystko co wchodzi od klienta → JSON.**

`print` jest dla Ciebie jako dewelopera — wypisuje do konsoli serwera. Klient tego nigdy nie zobaczy.

Trzy sposoby zwracania JSON w FastAPI:

```python
# 1. Słownik — zwracasz wprost
return {"total": 42, "status": "ok"}

# 2. Lista słowników
return [{"status": "todo", "count": 5}, {"status": "done", "count": 3}]

# 3. Obiekt SQLAlchemy — FastAPI + Pydantic zamieniają na JSON automatycznie
return db_user
```

**Wyjątek:** DELETE ze statusem `204 No Content` — jedyna sytuacja gdzie nic nie zwracasz.

| Co zwracasz | Jak | Kiedy |
|---|---|---|
| Słownik | `return {"klucz": wartość}` | statystyki, własne struktury |
| Lista słowników | `return [{"k": v} for ...]` | grupowania, agregacje |
| Obiekt SQLAlchemy | `return db_user` | standardowe endpointy CRUD |
| Nic | brak `return` | DELETE (204) |
