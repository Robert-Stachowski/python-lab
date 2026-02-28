# Ściągawka: Pydantic Schemas w FastAPI

## Po co w ogóle schematy?

Masz dwie warstwy w projekcie:
- **SQLAlchemy models** (`models.py`) → opisują **tabelę w bazie danych**
- **Pydantic schemas** (`schemas/`) → opisują **JSON przychodzący i wychodzący przez API**

To dwa różne światy. Schemat Pydantic jest "tłumaczem" między nimi.

```
Użytkownik → JSON → [Pydantic waliduje] → logika → [SQLAlchemy] → baza
Baza → [SQLAlchemy] → obiekt Python → [Pydantic serializuje] → JSON → Użytkownik
```

---

## Dlaczego trzy klasy na jeden model?

Każda klasa opisuje inną sytuację:

| Klasa | Kiedy używana | Co zawiera |
|---|---|---|
| `UserCreate` | POST - tworzenie | Dane od użytkownika. Bez `id`, `created_at` (baza je wygeneruje) |
| `UserUpdate` | PUT - aktualizacja | Wszystkie pola `Optional` — można zmienić jedno lub kilka |
| `UserResponse` | Odpowiedź API | To co zwracamy. Ma `id`, `created_at`. Ma `Config` |

### Przykład - User

```python
# Tworzenie — użytkownik podaje tylko to co zna
class UserCreate(BaseModel):
    username: str
    email: EmailStr        # EmailStr waliduje format emaila automatycznie

# Aktualizacja — wszystko Optional, bo można zmienić tylko jedno pole
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

# Odpowiedź — to co API zwraca, id i created_at już istnieją
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True   # ← TYLKO w Response, czyta atrybuty obiektów SQLAlchemy
```

---

## Dlaczego osobne pliki?

Nie wymóg techniczny — kwestia porządku.
4 modele × 3 klasy = 12 klas. W jednym pliku → chaos po miesiącu.

```
schemas/
  tag.py      ← TagCreate, TagResponse
  user.py     ← UserCreate, UserUpdate, UserResponse
  task.py     ← TaskCreate, TaskUpdate, TaskStatusUpdate, TaskResponse + Enumy
  project.py  ← ProjectCreate, ProjectUpdate, ProjectResponse, ProjectWithTasksResponse
  __init__.py ← eksportuje wszystko (patrz niżej)
```

Kolejność zależności (ważne przy importach!):
```
tag  ←  task  ←  project
user (niezależny)
```
`task.py` importuje z `tag.py`, `project.py` importuje z `task.py`.

---

## Config i from_attributes

```python
class UserResponse(BaseModel):
    id: int
    ...
    class Config:
        from_attributes = True
```

Pydantic domyślnie czyta tylko słowniki.
Baza danych zwraca **obiekty Python** (`<User id=1 username='jan'>`), nie słowniki.
`from_attributes = True` mówi Pydantic: "umiesz też czytać atrybuty obiektów".

**Tylko klasy Response mają Config** — tylko one czytają z obiektów SQLAlchemy.
`UserCreate` i `UserUpdate` czytają z JSON-a od użytkownika — nie potrzebują Config.

---

## Enum — walidacja dozwolonych wartości

Bez Enum użytkownik może wysłać `"zrobione"`, `"DONE"`, `"xyz"` — wszystko przejdzie.

```python
from enum import Enum

class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"
```

`str, Enum` — dziedziczy po obu, dzięki czemu wartości są stringami i można je porównywać.

Użycie w schemacie:
```python
class TaskCreate(BaseModel):
    status: TaskStatus = TaskStatus.todo      # domyślna wartość przez Enum
    priority: TaskPriority = TaskPriority.medium

class TaskUpdate(BaseModel):
    status: Optional[TaskStatus] = None       # opcjonalne, ale jeśli podane → walidowane

class TaskStatusUpdate(BaseModel):
    status: TaskStatus                        # wymagane, tylko dozwolone wartości
```

---

## Zagnieżdżone schematy (relacje)

Gdy model ma relację (np. Task ma tagi, Project ma zadania), Response zawiera zagnieżdżony schemat:

```python
# task.py
class TaskResponse(BaseModel):
    id: int
    title: str
    tags: List[TagResponse] = []   # ← lista zagnieżdżonych obiektów Tag
    ...
    class Config:
        from_attributes = True

# project.py
class ProjectWithTasksResponse(ProjectResponse):  # ← dziedziczy z ProjectResponse
    tasks: List[TaskResponse] = []                # ← dodaje listę zadań
```

`ProjectWithTasksResponse` dziedziczy WSZYSTKIE pola z `ProjectResponse` i dodaje `tasks`.
Używany tylko dla `GET /projects/{id}` — szczegółowy widok z zadaniami.
Zwykły `GET /projects` używa `ProjectResponse` — bez zadań (szybsze zapytanie).

---

## __init__.py — jeden punkt importu

Bez `__init__.py`:
```python
from app.schemas.user import UserCreate          # trzeba znać strukturę plików
from app.schemas.task import TaskResponse, TaskStatus
```

Z `__init__.py`:
```python
from app.schemas import UserCreate, TaskResponse, TaskStatus   # prosto
```

Zawartość `__init__.py` (kolejność: od najmniej do najbardziej zależnych):
```python
from .tag import TagCreate, TagResponse
from .user import UserCreate, UserUpdate, UserResponse
from .task import TaskStatus, TaskPriority, TaskCreate, TaskUpdate, TaskStatusUpdate, TaskResponse
from .project import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectWithTasksResponse
```

---

## Jak schemat jest używany w routerze

```python
@router.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    #            ↑ schemat wejścia         ↑ schemat wyjścia (w dekoratorze)
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user   # FastAPI przepuści przez UserResponse automatycznie
```

- `user: UserCreate` → Pydantic waliduje JSON z requestu, błąd = 422
- `response_model=UserResponse` → Pydantic filtruje i serializuje odpowiedź, dokumentuje w Swaggerze
- `user.model_dump()` → zamienia schemat Pydantic na słownik, `**` rozpakowuje do kwargs

---

## Pełny przepływ requestu

```
1. Użytkownik → POST /users  {"username": "jan", "email": "jan@example.com"}
2. FastAPI → waliduje przez UserCreate (EmailStr sprawdza email)
3. Jeśli błąd → 422 Unprocessable Entity (automatycznie)
4. Jeśli OK → wywołuje funkcję create_user(user=UserCreate(...), db=Session)
5. Funkcja → tworzy obiekt User, zapisuje do bazy
6. Funkcja → zwraca obiekt SQLAlchemy User
7. FastAPI → przepuszcza przez UserResponse (from_attributes=True czyta atrybuty)
8. Użytkownik ← {"id": 1, "username": "jan", "email": "jan@example.com", ...}
```

---

## Szybka ściąga — typy Pydantic

| Typ | Zastosowanie |
|---|---|
| `str` | Zwykły tekst |
| `int` | Liczba całkowita |
| `bool` | True/False |
| `datetime` | Data i czas |
| `date` | Tylko data |
| `Optional[str]` | String lub None (= `str \| None`) |
| `EmailStr` | String walidowany jako email (wymaga `pydantic[email]`) |
| `List[TagResponse]` | Lista obiektów danego schematu |
| `TaskStatus` | Enum — tylko dozwolone wartości |
