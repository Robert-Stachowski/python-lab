# Ściągawka: main.py w FastAPI

## Po co w ogóle main.py?

`main.py` to **punkt wejścia całej aplikacji** — pierwsze co uruchamia się gdy startujesz serwer.
Nie zawiera logiki biznesowej ani zapytań do bazy. Robi trzy rzeczy:

1. **Tworzy aplikację** FastAPI
2. **Uruchamia tabele** w bazie przy starcie
3. **Podłącza routery** — rejestruje wszystkie endpointy

Analogia: `main.py` to recepcja hotelu — nie obsługuje gości, tylko kieruje ich do odpowiednich pięter.

---

## Miejsce main.py w architekturze

```
HTTP Request
     ↓
main.py          ← punkt wejścia, podłącza routery
     ↓
routers/         ← logika endpointu
     ↓
schemas/         ← walidacja i serializacja (Pydantic)
     ↓
models.py        ← zapis i odczyt z bazy (SQLAlchemy)
     ↓
PostgreSQL
```

---

## Pełny plik main.py — linijka po linijce

```python
from fastapi import FastAPI
from .database import Base, engine
from . import models
from .routers import users, projects, tasks, tags, stats

app = FastAPI(
    title="Task Manager API",
    description="REST API do zarzadzania zadaniami - projekt portfolio",
    version="1.0.0",
)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

app.include_router(users.router,    prefix="/users",    tags=["Users"])
app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(tasks.router,    prefix="/tasks",    tags=["Tasks"])
app.include_router(tags.router,     prefix="/tags",     tags=["Tags"])
app.include_router(stats.router,    prefix="/stats",    tags=["Stats"])

@app.get("/")
def root():
    return {"message": "Task Manager API", "docs": "/docs"}
```

---

## Importy — co i po co

```python
from fastapi import FastAPI
```
Importujesz klasę `FastAPI` — to jest serce całej aplikacji. Bez tego nie ma serwera.

---

```python
from .database import Base, engine
```
- `Base` — potrzebna do `create_all()` — wie o wszystkich modelach które po niej dziedziczą
- `engine` — połączenie z PostgreSQL — wie jak dostać się do bazy

---

```python
from . import models
```
Ładuje wszystkie modele do pamięci. Bez tego `Base.metadata.create_all()` **nie wie jakie tabele tworzyć**.

Modele muszą być załadowane żeby "zarejestrowały się" w `Base`. Ten import wygląda na nieużywany — ale jest niezbędny. Nie usuwaj go.

---

```python
from .routers import users, projects, tasks, tags, stats
```
Importujesz wszystkie pliki routerów. Każdy z nich ma obiekt `router = APIRouter()` z zarejestrowanymi endpointami.

---

## Tworzenie aplikacji

```python
app = FastAPI(
    title="Task Manager API",
    description="REST API do zarzadzania zadaniami - projekt portfolio",
    version="1.0.0",
)
```

Tworzysz instancję aplikacji. `title`, `description` i `version` pojawiają się automatycznie w **Swagger UI** pod adresem `/docs` — dokumentacja Twojego API generowana za darmo przez FastAPI.

---

## Startup event — tworzenie tabel

```python
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
```

`@app.on_event("startup")` — dekorator który mówi FastAPI:
*"uruchom tę funkcję zaraz po starcie serwera, zanim przyjmie pierwszy request"*

`Base.metadata.create_all(bind=engine)` — sprawdza jakie tabele są zdefiniowane w modelach i tworzy je w bazie jeśli nie istnieją. Jeśli już istnieją — nic nie robi. Bezpieczne przy każdym restarcie.

Kolejność działania przy starcie serwera:
```
serwer startuje
     ↓
@app.on_event("startup") → tworzenie tabel w bazie
     ↓
serwer gotowy na requesty
```

---

## include_router — podłączanie routerów

```python
app.include_router(users.router, prefix="/users", tags=["Users"])
```

Trzy argumenty:

| Argument | Co robi |
|---|---|
| `users.router` | podłącza obiekt `router` z pliku `users.py` |
| `prefix="/users"` | dodaje przedrostek do wszystkich URL w routerze |
| `tags=["Users"]` | grupuje endpointy pod wspólną etykietą w Swagger UI |

### Jak działa prefix?

W `users.py` piszesz:
```python
@router.get("/")        # nie "/users/"
@router.get("/{id}")    # nie "/users/{id}"
```

Prefix `/users` jest dodawany dopiero w `main.py`:
```
router.get("/")       + prefix="/users"  →  GET /users/
router.get("/{id}")   + prefix="/users"  →  GET /users/{id}
```

Dzięki temu router nie wie nic o swojej ścieżce — jest przenośny i niezależny.

---

## Endpoint powitalny

```python
@app.get("/")
def root():
    return {"message": "Task Manager API", "docs": "/docs"}
```

Prosty endpoint na głównym adresie `/`. Gdy ktoś wejdzie na adres API dostaje informację że serwer działa i gdzie jest dokumentacja.

Uwaga: ten endpoint jest bezpośrednio w `main.py`, nie w żadnym routerze — bo nie należy do żadnego zasobu.

---

## Swagger UI — darmowa dokumentacja

FastAPI automatycznie generuje interaktywną dokumentację pod adresem:

```
http://localhost:8000/docs
```

Widać tam:
- wszystkie endpointy pogrupowane przez `tags`
- wymagane parametry i body każdego endpointu
- możliwość testowania API bezpośrednio z przeglądarki
- `title`, `description`, `version` z `FastAPI()`

Nie musisz nic pisać — dokumentacja tworzy się sama na podstawie kodu.

---

## Jak uruchomić serwer

```bash
uvicorn app.main:app --reload
```

- `app.main` — ścieżka do pliku (katalog `app`, plik `main.py`)
- `:app` — nazwa obiektu FastAPI w tym pliku
- `--reload` — serwer restartuje się automatycznie po każdej zmianie kodu (tylko development)

---

## Zestawienie — co robi każda część main.py

| Co | Po co |
|---|---|
| `app = FastAPI()` | tworzy aplikację |
| `title, description, version` | metadane widoczne w Swagger UI |
| `from . import models` | rejestruje modele w Base (niewidocznie ale niezbędne) |
| `@app.on_event("startup")` | kod uruchamiany raz przy starcie serwera |
| `Base.metadata.create_all()` | tworzy tabele w bazie jeśli nie istnieją |
| `include_router()` | podłącza router do aplikacji |
| `prefix` | dodaje przedrostek do wszystkich URL routera |
| `tags` | grupuje endpointy w Swagger UI |
| `@app.get("/")` | endpoint powitalny — sprawdzenie że serwer działa |
