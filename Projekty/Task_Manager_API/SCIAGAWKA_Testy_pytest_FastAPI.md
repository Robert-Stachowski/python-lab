# Ściągawka: Testy automatyczne w FastAPI (pytest)

---

## 1. Po co w ogóle testy automatyczne?

Bez testów po każdej zmianie w kodzie musisz ręcznie otwierać Swagger UI i klikać każdy endpoint.
Przy 5 endpointach — da się. Przy 30 — to koszmar.

Testy automatyczne robią to za Ciebie. Jedno polecenie:

```bash
pytest
```

...i w kilka sekund wiesz, czy wszystko działa.

---

## 2. Trzy problemy do rozwiązania

Zanim zaczniesz pisać testy, musisz odpowiedzieć na trzy pytania:

| Problem | Pytanie | Nasze rozwiązanie |
|---|---|---|
| Jak wysyłać requesty bez uruchamiania serwera? | Muszę mieć coś zamiast `uvicorn` | **TestClient** |
| Jak nie niszczyć produkcyjnej bazy danych? | Testy tworzą i usuwają dane — nie mogę dotknąć PostgreSQL | **SQLite in-memory** |
| Jak powiedzieć aplikacji żeby używała testowej bazy? | Aplikacja zawsze łączy się z PostgreSQL przez `get_db` | **dependency_overrides** |

---

## 3. TestClient — serwer tylko na niby

FastAPI dostarcza `TestClient` — specjalny klient HTTP który:
- symuluje prawdziwe requesty HTTP (`GET`, `POST`, `DELETE`...)
- **nie uruchamia żadnego serwera** — nie potrzebujesz `uvicorn`
- działa synchronicznie — pytest może go normalnie używać

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

response = client.get("/users")          # tak jakbyś wpisał GET /users w Swagger
response = client.post("/users/", json={"username": "jan", "email": "jan@example.com"})
```

To dosłownie jak `requests.get(...)` — tylko bez prawdziwego serwera w tle.

---

## 4. Dlaczego NIE używamy Mocka?

### Co to jest Mock?

Mock to fałszywy obiekt, który **udaje** bazę danych. Zamiast prawdziwej sesji SQLAlchemy, dajesz testowi obiekt który mówi:

> "Kiedy ktoś wywoła `.query(User).all()`, zwróć tę listę którą ja przygotowałem."

```python
# Przykład — jak WYGLĄDAŁBY mock bazy danych
mock_db.query.return_value.all.return_value = [fake_user1, fake_user2]
```

### Dlaczego Mock jest złym pomysłem przy testach endpointów?

Mock sprawdza tylko **czy Twój kod wywołał odpowiednie metody**.
Nie sprawdza **czy te metody naprawdę działają**.

Analogia z życia:
> Mock to jak egzamin dla kucharza, gdzie zamiast gotowania sprawdzamy czy kandydat **wymawia odpowiednie słowa** w odpowiedniej kolejności.
> Może powiedzieć "sól → pieprz → mieszam" i zda. Ale czy zupa będzie dobra? Nie wiadomo.

### Co Mock pominie — a SQLite sprawdzi?

| Co testujemy | Mock | SQLite in-memory |
|---|---|---|
| Relacja N:M (task_tag) | ❌ nie testuje | ✅ naprawdę zapisuje |
| Cascade delete (projekt → taski) | ❌ nie testuje | ✅ naprawdę kasuje |
| UNIQUE constraint (duplikat emaila) | ❌ nie testuje | ✅ naprawdę rzuca błąd |
| Filtrowanie przez Query (status, priority) | ❌ nie testuje | ✅ naprawdę filtruje |
| Relacje przez `selectinload` | ❌ nie testuje | ✅ naprawdę ładuje |

**Wniosek:** Mock nadaje się do testowania logiki biznesowej odizolowanej od bazy.
Do testowania endpointów REST API — Mock to zły wybór.

---

## 5. SQLite in-memory — tymczasowa baza w RAM

SQLite to lekka baza danych wbudowana w Pythona — zero instalacji, zero konfiguracji.

Tryb `in-memory` oznacza że baza:
- **powstaje w RAM** przy starcie testu
- **znika z RAM** gdy test się kończy
- nie zostawia żadnych plików na dysku
- każdy test startuje z czystym stanem

```python
# Plikowa — ZŁY wybór dla testów
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"   # tworzy plik test.db na dysku

# In-memory — DOBRY wybór dla testów
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"    # tylko w RAM, znika po teście
```

### Dlaczego nie zostawiamy pliku na dysku?

- Plik zostaje po teście — następny test zaczyna z brudnymi danymi
- Trzeba ręcznie sprzątać
- Na CI/CD (GitHub Actions) plik może zostać między uruchomieniami

In-memory = zawsze czysto, zawsze izolacja.

### Ważny szczegół dla SQLite + FastAPI

SQLite domyślnie nie pozwala używać jednego połączenia z wielu wątków.
FastAPI może obsługiwać requesty w wielu wątkach — dlatego musisz dodać jeden argument:

```python
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False}   # wymagane dla SQLite w FastAPI
)
```

Bez tego dostaniesz błąd przy pierwszym requeście.

---

## 6. Dlaczego nadpisujemy `get_db`?

### Jak aplikacja normalnie łączy się z bazą?

W każdym routerze widzisz:

```python
def get_users(db: Session = Depends(get_db)):
    ...
```

`Depends(get_db)` to mechanizm Dependency Injection — FastAPI automatycznie wywołuje `get_db()` i wstrzykuje sesję do funkcji.

`get_db` w `database.py` wygląda tak:

```python
def get_db():
    db = SessionLocal()   # ← SessionLocal to sesja PostgreSQL
    try:
        yield db
    finally:
        db.close()
```

### Problem

Gdy testujesz endpoint, FastAPI wywoła `get_db()` i dostanie sesję **PostgreSQL**.
Chcesz żeby dostał sesję **SQLite in-memory**.

### Rozwiązanie: `dependency_overrides`

FastAPI ma słownik `app.dependency_overrides`. Możesz do niego wpisać:

> "Kiedy ktokolwiek prosi o `get_db`, daj mu **moją funkcję** zamiast prawdziwej."

```python
def override_get_db():
    yield testowa_sesja_sqlite   # ← zamiast PostgreSQL

app.dependency_overrides[get_db] = override_get_db
```

Od tego momentu każdy endpoint który robi `Depends(get_db)` dostanie SQLite zamiast PostgreSQL.
Gdy test się kończy — czyścimy:

```python
app.dependency_overrides.clear()   # przywróć oryginał po teście
```

---

## 7. Fixtures i conftest.py

### Co to jest fixture?

Fixture to funkcja która **przygotowuje coś przed testem i sprząta po nim**.

Analogia z życia:
> Kelner (fixture) nakrywa stół przed posiłkiem i sprząta po.
> Ty (test) tylko jesz — nie martwisz się o talerze.

```python
@pytest.fixture
def client(db):
    # SETUP — przed testem
    def override_get_db():
        yield db
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c   # ← tu wykonuje się test

    # TEARDOWN — po teście
    app.dependency_overrides.clear()
```

### Jak test używa fixture?

Wystarczy wpisać nazwę fixture jako argument funkcji testowej — pytest sam to wstrzyknie:

```python
def test_create_user(client):   # ← "client" to fixture z conftest.py
    response = client.post("/users/", json={
        "username": "jan",
        "email": "jan@example.com"
    })
    assert response.status_code == 201
```

Nie importujesz fixture. Pytest sam go znajdzie w `conftest.py`.

### Co to jest `conftest.py`?

`conftest.py` to specjalny plik pytest który:
- jest **automatycznie wczytywany** przez pytest (bez importowania)
- zawiera fixtures **współdzielone przez wszystkie pliki testów**
- żyje w katalogu `tests/`

Jeśli masz fixture w `conftest.py`, możesz go użyć w `test_users.py`, `test_projects.py` i `test_tasks.py` — bez żadnych importów.

### Dwie fixtures w conftest.py

```
db     ← tworzy SQLite in-memory, tworzy tabele, sprząta po teście
client ← nadpisuje get_db, tworzy TestClient, czyści overrides po teście
```

`client` zależy od `db` — dlatego `db` jest argumentem `client`.
Pytest automatycznie uruchomi `db` przed `client`.

---

## 8. Pełny przepływ jednego testu

```
pytest uruchamia test_create_user(client)
        ↓
pytest szuka fixture "client" w conftest.py
        ↓
"client" potrzebuje "db" → pytest uruchamia fixture "db"
        ↓
fixture db: tworzy SQLite in-memory, tworzy wszystkie tabele (Base.metadata.create_all)
        ↓
fixture client: nadpisuje get_db → teraz wskazuje na SQLite; tworzy TestClient
        ↓
yield → wykonuje się test_create_user
        ↓
test robi: client.post("/users/", json={...})
        ↓
TestClient wysyła request do FastAPI (bez serwera)
        ↓
FastAPI przetwarza request, pyta o bazę przez Depends(get_db)
        ↓
dependency_overrides przekierowuje → dostaje sesję SQLite zamiast PostgreSQL
        ↓
router zapisuje użytkownika do SQLite in-memory
        ↓
FastAPI zwraca response → test sprawdza assert response.status_code == 201
        ↓
fixture client sprząta: dependency_overrides.clear()
        ↓
fixture db sprząta: session.close(), Base.metadata.drop_all (usuwa tabele z RAM)
        ↓
baza znika z RAM — czysto na następny test
```

---

## 9. Struktura conftest.py — gotowy wzorzec

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

# Testowa baza — SQLite in-memory
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # wymagane dla SQLite + FastAPI
)
TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)   # utwórz tabele przed testem
    session = TestingSessionLocal()
    try:
        yield session                        # oddaj sesję testowi
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine) # usuń tabele po teście


@pytest.fixture
def client(db):
    def override_get_db():
        yield db                             # zamiast PostgreSQL daj SQLite
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c                              # oddaj klienta testowi
    app.dependency_overrides.clear()        # posprzątaj po teście
```

---

## 10. Struktura testu — wzorzec AAA

Każdy test powinien mieć trzy sekcje:

```python
def test_create_user(client):
    # ARRANGE — przygotuj dane wejściowe
    payload = {"username": "jan", "email": "jan@example.com"}

    # ACT — wykonaj akcję
    response = client.post("/users/", json=payload)

    # ASSERT — sprawdź wynik
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "jan"
    assert data["email"] == "jan@example.com"
    assert data["is_active"] == True
```

**Arrange** → przygotuj dane
**Act** → wykonaj request
**Assert** → sprawdź odpowiedź

---

## 11. Zestawienie — skąd co pochodzi

| Element | Skąd | Co robi |
|---|---|---|
| `TestClient` | `fastapi.testclient` | Symuluje HTTP bez serwera |
| `pytest.fixture` | `pytest` | Dekorator — oznacza funkcję jako fixture |
| `conftest.py` | pytest (konwencja) | Plik z fixtures współdzielonymi przez wszystkie testy |
| `dependency_overrides` | FastAPI (`app`) | Podmienia dowolną zależność w testach |
| `Base.metadata.create_all` | SQLAlchemy | Tworzy tabele w testowej bazie |
| `Base.metadata.drop_all` | SQLAlchemy | Usuwa tabele po teście |
| `sqlite:///:memory:` | SQLAlchemy (URL) | Baza w RAM, znika po teście |
| `check_same_thread: False` | SQLite | Pozwala używać połączenia z wielu wątków |
| `yield` w fixture | Python | Punkt wykonania testu — przed = setup, po = teardown |

---

## 12. Najczęstsze błędy

| Błąd | Przyczyna | Rozwiązanie |
|---|---|---|
| `sqlite:///:memory:` a dane z poprzedniego testu | Używasz `sqlite:///./test.db` (plik!) | Zmień na `sqlite:///:memory:` |
| `check_same_thread` error | Brak `connect_args` | Dodaj `connect_args={"check_same_thread": False}` |
| Fixture nie znaleziony | Fixture nie jest w `conftest.py` | Przenieś fixture do `conftest.py` |
| 422 zamiast 201 | Zły format JSON w teście | Sprawdź pola wymagane w schemacie `Create` |
| dependency_overrides nie działa | Importujesz `get_db` z innego miejsca | Upewnij się że importujesz z `app.database` |
