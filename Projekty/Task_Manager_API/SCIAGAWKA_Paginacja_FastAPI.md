# Ściągawka: Paginacja w FastAPI

## Po co w ogóle paginacja?

Wyobraź sobie że masz w bazie 50 000 zadań. Klient robi `GET /tasks/` i serwer
próbuje zwrócić wszystko naraz. Efekt:

- Serwer ładuje 50 000 obiektów do pamięci RAM
- Odpowiedź waży dziesiątki MB
- Baza danych ciężko pracuje bez potrzeby
- Frontend dostaje za dużo danych i nie wie co z nimi zrobić

**Paginacja** dzieli wyniki na strony — serwer zwraca tylko kawałek, a klient
sam decyduje którą "stronę" chce zobaczyć.

---

## Miejsce paginacji w architekturze

```
HTTP Request: GET /tasks/?skip=20&limit=10
     ↓
router (tasks.py)    ← odbiera parametry skip i limit z URL-a
     ↓
SQLAlchemy query     ← .offset(skip).limit(limit)
     ↓
PostgreSQL           ← SELECT ... OFFSET 20 LIMIT 10
     ↓
Response             ← {"total": 50000, "skip": 20, "limit": 10, "items": [...]}
```

---

## Dwa parametry paginacji

| Parametr | Co robi | Domyślna wartość |
|---|---|---|
| `skip` | ile rekordów pominąć od początku | 0 |
| `limit` | ile rekordów zwrócić | np. 10 |

**Wzór na numer strony:**
```
skip = (numer_strony - 1) * limit
```

**Przykład — 50 000 zadań, strony po 10:**
```
GET /tasks/?skip=0&limit=10   → rekordy   1–10  (strona 1)
GET /tasks/?skip=10&limit=10  → rekordy  11–20  (strona 2)
GET /tasks/?skip=20&limit=10  → rekordy  21–30  (strona 3)
GET /tasks/?skip=490&limit=10 → rekordy 491–500 (strona 50)
```

---

## Parametry Query w FastAPI

FastAPI czyta parametry z URL-a automatycznie — wystarczy dodać je do funkcji.
To działa tak samo jak filtry które znasz z `tasks.py`.

```python
# Bez paginacji (mamy teraz)
@router.get("/")
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()

# Z paginacją
@router.get("/")
def get_tasks(
    skip: int = 0,       # domyślnie: zacznij od początku
    limit: int = 10,     # domyślnie: zwróć 10 rekordów
    db: Session = Depends(get_db)
):
    return db.query(Task).offset(skip).limit(limit).all()
```

FastAPI sam:
- czyta `skip` i `limit` z URL-a
- waliduje że to liczby całkowite (`int`)
- używa wartości domyślnych jeśli klient ich nie podał

---

## SQLAlchemy: offset i limit

```python
db.query(Task).all()
# SELECT * FROM tasks
# → zwraca WSZYSTKIE rekordy

db.query(Task).offset(20).limit(10).all()
# SELECT * FROM tasks OFFSET 20 LIMIT 10
# → pomija pierwsze 20, zwraca kolejne 10
```

Kolejność ma znaczenie: zawsze najpierw `.offset()`, potem `.limit()`, na końcu `.all()`.

Można łączyć z filtrami:
```python
db.query(Task)\
  .filter(Task.status == "todo")\
  .offset(skip)\
  .limit(limit)\
  .all()
```

---

## Dwa style odpowiedzi

### Styl prosty — sama lista (mamy teraz)

```json
[
  {"id": 1, "title": "Zadanie pierwsze"},
  {"id": 2, "title": "Zadanie drugie"}
]
```

Wada: klient nie wie ile jest wszystkich rekordów — nie może narysować
przycisków "strona 1 z 500".

### Styl profesjonalny — lista + metadane

```json
{
  "total": 50000,
  "skip": 20,
  "limit": 10,
  "items": [
    {"id": 21, "title": "Zadanie dwudzieste pierwsze"},
    {"id": 22, "title": "Zadanie dwudzieste drugie"}
  ]
}
```

Zaleta: klient wie wszystko — ile stron, gdzie jest teraz, ile rekordów łącznie.

---

## Schema odpowiedzi z metadanymi

Żeby FastAPI wiedział jak ma wyglądać odpowiedź, trzeba stworzyć schemat Pydantic:

```python
# schemas/pagination.py

from pydantic import BaseModel
from typing import Generic, TypeVar, List

T = TypeVar("T")  # T to "placeholder" na dowolny typ

class PaginatedResponse(BaseModel, Generic[T]):
    total: int
    skip: int
    limit: int
    items: List[T]
```

`Generic[T]` oznacza że ten schemat działa dla dowolnego typu — raz `T` to
`TaskResponse`, innym razem `UserResponse`. Jeden schemat dla wszystkich list.

**Użycie w endpointcie:**

```python
from schemas.pagination import PaginatedResponse
from schemas.task import TaskResponse

@router.get("/", response_model=PaginatedResponse[TaskResponse])
def get_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    total = db.query(Task).count()   # COUNT(*) — ile wszystkich rekordów
    items = db.query(Task).offset(skip).limit(limit).all()

    return PaginatedResponse(
        total=total,
        skip=skip,
        limit=limit,
        items=items
    )
```

---

## Liczenie wszystkich rekordów: .count()

```python
db.query(Task).count()
# SELECT COUNT(*) FROM tasks
# → zwraca liczbę całkowitą (int), np. 50000

# Z filtrem:
db.query(Task).filter(Task.status == "todo").count()
# SELECT COUNT(*) FROM tasks WHERE status = 'todo'
```

Ważne: `total` liczymy PRZED zastosowaniem `offset` i `limit` — chcemy
wiedzieć ile jest wszystkich pasujących rekordów, nie tylko tych na stronie.

---

## Walidacja parametrów — zabezpieczenie przed błędami

Co jeśli klient poda `limit=99999`? Serwer zwróci prawie wszystko.
FastAPI pozwala dodać ograniczenia bezpośrednio w sygnaturze funkcji:

```python
from fastapi import Query

def get_tasks(
    skip: int = Query(default=0, ge=0),           # ge=0: skip >= 0
    limit: int = Query(default=10, ge=1, le=100)  # limit: od 1 do 100
):
    ...
```

| Parametr | Znaczenie |
|---|---|
| `ge=0` | greater or equal — wartość >= 0 |
| `le=100` | less or equal — wartość <= 100 |
| `gt=0` | greater than — wartość > 0 |
| `lt=100` | less than — wartość < 100 |

FastAPI automatycznie zwróci `422 Unprocessable Entity` jeśli klient poda
wartość poza zakresem.

---

## Paginacja z istniejącymi filtrami

Nasze `GET /tasks/` już ma filtry (`status`, `priority`). Paginacja dokłada się
na to bez konfliktu:

```python
@router.get("/", response_model=PaginatedResponse[TaskResponse])
def get_tasks(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Task)

    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)

    total = query.count()                          # liczymy po filtrach, przed paginacją
    items = query.offset(skip).limit(limit).all()  # paginacja na końcu

    return PaginatedResponse(total=total, skip=skip, limit=limit, items=items)
```

Kluczowa kolejność:
1. Zbuduj query bazową
2. Dodaj filtry
3. Policz `total` (po filtrach, przed paginacją)
4. Dodaj `offset` i `limit`
5. Wywołaj `.all()`

---

## Zestawienie — wszystko w jednym miejscu

```
URL:      GET /tasks/?skip=20&limit=10&status=todo

FastAPI:  skip: int = Query(default=0, ge=0)
          limit: int = Query(default=10, ge=1, le=100)
          → automatyczna walidacja i wartości domyślne

SQLAlchemy:
          query = db.query(Task).filter(Task.status == "todo")
          total = query.count()               ← COUNT(*) po filtrach
          items = query.offset(20).limit(10).all()  ← 10 rekordów od pozycji 20

Odpowiedź:
          {
            "total": 347,   ← ile zadań "todo" jest w bazie
            "skip": 20,
            "limit": 10,
            "items": [...]  ← 10 zadań
          }

Schema:   PaginatedResponse[TaskResponse]
          → Generic[T] — jeden schemat dla wszystkich list
```

---

## Gdzie dodać paginację w projekcie

| Endpoint | Paginacja |
|---|---|
| `GET /tasks/` | TAK — główny kandydat, może mieć dużo rekordów |
| `GET /users/` | TAK — lista użytkowników |
| `GET /projects/` | TAK — lista projektów |
| `GET /tags/` | TAK — lista tagów |
| `GET /tasks/{id}` | NIE — zawsze jeden rekord |
| `GET /projects/{id}` | NIE — zawsze jeden rekord |
| `GET /stats/...` | NIE — agregacje, nie listy rekordów |
