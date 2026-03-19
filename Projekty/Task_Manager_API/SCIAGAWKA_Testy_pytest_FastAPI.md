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
| `{"owner_id": {user_id}}` — błąd serializacji | `{user_id}` to set Pythona, nie liczba | Usuń nawiasy klamrowe: `"owner_id": user_id` |

---

## 13. Zagnieżdżone fixtures — dane testowe

Zamiast ręcznie tworzyć usera i projekt w każdym teście, możesz zrobić **fixtures z danymi**.
Wrzucasz je do `conftest.py` — są dostępne we wszystkich plikach testów bez importu.

```python
@pytest.fixture
def test_user(client):
    response = client.post("/users/", json={
        "username": "testuser",
        "email": "test@example.com"
    })
    return response.json()   # ← zwraca gotowy słownik, nie surowy response


@pytest.fixture
def test_project(client, test_user):   # ← zależy od test_user
    response = client.post("/projects/", json={
        "name": "Test projekt",
        "description": "Opis projektu",
        "owner_id": test_user["id"]    # ← automatycznie bierze id z test_user
    })
    return response.json()
```

### Jak pytest ogarnia kolejność?

`test_project` ma w argumentach `test_user` — pytest widzi tę zależność i uruchamia fixtures w odpowiedniej kolejności:

```
db → client → test_user → test_project → test
```

### Jak użyć w teście?

```python
def test_create_task(client, test_project, test_user):
    response = client.post("/tasks/", json={
        "title": "Moje zadanie",
        "project_id": test_project["id"],   # ← gotowe, bez ręcznego tworzenia
        "assignee_id": test_user["id"]
    })
    assert response.status_code == 201
```

### Kiedy fixture, kiedy ręcznie?

| Sytuacja | Podejście |
|---|---|
| Dane potrzebne w więcej niż jednym teście | Fixture w `conftest.py` |
| Dane potrzebne tylko w tym jednym teście | Ręcznie w teście |
| Test sprawdza samo tworzenie obiektu | Ręcznie — fixture ukryłby to co testujesz |

### Fixtures zwracają gotowe słowniki — nie potrzebujesz GET

Gdy używasz `test_user` i `test_project` w teście, dane są **już dostępne** — fixtures zwróciły `response.json()`.
Nie musisz robić dodatkowych requestów GET żeby pobrać dane z bazy:

```python
# ŹLE — zbędny request, dane już masz w fixture
response = client.get(f"/users/{test_user['id']}")
data = response.json()
assert data["username"] == "testuser"

# DOBRZE — fixture już zwróciła gotowy słownik
assert test_user["username"] == "testuser"
assert test_project["name"] == "Test projekt"
assert test_project["owner_id"] == test_user["id"]  # sprawdzasz relację
```

### Czy `client` musi być w argumentach jeśli nie używasz go w ciele testu?

Nie — możesz go pominąć. Pytest sam ogarnie łańcuch zależności:

```python
# Działa — pytest wie że test_project potrzebuje client i db
def test_create_project(test_project, test_user):
    assert test_project["name"] == "Test projekt"
    assert test_project["owner_id"] == test_user["id"]

# Też działa — client jawnie w argumentach (potrzebny gdy robisz requesty w teście)
def test_create_task(client, test_project, test_user):
    response = client.post("/tasks/", json={...})
    ...
```

**Zasada:** jeśli w ciele testu używasz `client.get(...)` / `client.post(...)` — dodaj `client` do argumentów.
Jeśli tylko sprawdzasz dane z fixtures — `client` możesz pominąć.

---

## 14. Odpytywanie listy — indeksy i klucze

Endpointy `GET /tasks/`, `GET /users/` itp. zwracają **listę** (nawet gdy jest jeden element).

```python
response = client.get("/tasks/")
data = response.json()
# data to lista:  [{"id": 1, "title": "...", "status": "todo"}, ...]
```

Żeby dostać się do konkretnego elementu i jego pola:

```python
data[0]              # pierwszy element listy (słownik)
data[0]["status"]    # wartość klucza "status" z pierwszego elementu
data[0]["title"]     # wartość klucza "title" z pierwszego elementu
```

Typowe asercje dla endpointu zwracającego listę:

```python
assert len(data) == 1              # na liście jest dokładnie 1 element
assert data[0]["status"] == "todo" # ten element ma właściwy status
assert data[0]["project_id"] == project_id  # ma właściwe id projektu
```

### Dostęp do zagnieżdżonych danych — relacje w response

Niektóre endpointy zwracają obiekt z zagnieżdżoną listą powiązanych obiektów.
Np. `GET /projects/{id}` zwraca projekt **razem z jego taskami** (`ProjectWithTasksResponse`):

```json
{
    "id": 1,
    "name": "Test projekt",
    "owner_id": 1,
    "tasks": [
        {"id": 1, "title": "Moje zadanie", "status": "todo"},
        {"id": 2, "title": "Drugie zadanie", "status": "done"}
    ]
}
```

Żeby dostać się do danych z zagnieżdżonej listy:

```python
data = response.json()

data["tasks"]              # cała lista tasków
data["tasks"][0]           # pierwszy task (słownik)
data["tasks"][0]["title"]  # tytuł pierwszego taska

# BŁĄD — tak nie działa, to nie jest poprawny klucz
data["tasks.title"]        # ❌ KeyError
```

Typowe asercje dla endpointu z zagnieżdżoną listą:

```python
data_project = client.get(f"/projects/{project_id}").json()

assert data_project["name"] == "Test projekt"
assert data_project["owner_id"] == test_user["id"]
assert len(data_project["tasks"]) == 1                          # jeden task w projekcie
assert data_project["tasks"][0]["title"] == "Moje zadanie"      # tytuł tego taska
```

---

### Parametry query — jak przekazać?

`GET /tasks/?status=todo` — parametry query to **nie jest body**, więc nie używasz `json=`.
Używasz `params=`:

```python
# ŹLE — json to body requestu (POST/PUT)
client.get("/tasks/", json={"status": "todo"})

# DOBRZE — params to parametry URL
client.get("/tasks/", params={"status": "todo"})
# TestClient zamienia to na: GET /tasks/?status=todo
```

Możesz przekazać wiele parametrów naraz:

```python
client.get("/tasks/", params={"status": "todo", "priority": "high"})
# → GET /tasks/?status=todo&priority=high
```

---

## 15. Testowanie relacji

### Cascade delete — co sprawdzić po usunięciu?

Gdy usuwasz obiekt nadrzędny (np. projekt), baza powinna automatycznie usunąć obiekty zależne (taski).
W teście sprawdzasz **oba** — rodzica i dziecko:

```python
def test_delete_project_cascades_tasks(client, test_project, test_user):
    # Utwórz taska w projekcie
    response = client.post("/tasks/", json={
        "title": "Zadanie",
        "project_id": test_project["id"],
        "assignee_id": test_user["id"]
    })
    task_id = response.json()["id"]
    project_id = test_project["id"]

    # Usuń projekt
    delete = client.delete(f"/projects/{project_id}")
    assert delete.status_code == 204

    # Sprawdź że projekt zniknął
    assert client.get(f"/projects/{project_id}").status_code == 404

    # Sprawdź że task też zniknął (cascade delete)
    assert client.get(f"/tasks/{task_id}").status_code == 404
```

### Relacja N:M — dodawanie taga do taska

Przy relacji wiele-do-wielu (task ↔ tag) masz dwa osobne kroki:
1. Stwórz tag przez `POST /tags/`
2. Przypisz tag do taska przez `POST /tasks/{id}/tags`

```python
def test_add_tag_to_task(client, test_project, test_user):
    # Utwórz taska
    response = client.post("/tasks/", json={
        "title": "Zadanie",
        "project_id": test_project["id"],
        "assignee_id": test_user["id"]
    })
    task_id = response.json()["id"]

    # Utwórz tag
    tag_data = {"name": "backend"}
    add_tag = client.post("/tags/", json=tag_data)
    assert add_tag.status_code == 201

    # Przypisz tag do taska
    assign = client.post(f"/tasks/{task_id}/tags", json=tag_data)
    assert assign.status_code == 201
    assert assign.json()["name"] == "backend"
```

### PATCH do zmiany statusu — f-string w URL

Endpoint zmiany statusu wymaga `task_id` w URL — używasz f-stringa:

```python
update_status = {"status": "done"}
response = client.patch(f"/tasks/{task_id}/status", json=update_status)
assert response.status_code == 200
assert response.json()["status"] == "done"
```

**Bez f-stringa** `"/tasks/{task_id}/status"` to dosłowny string — FastAPI nie znajdzie takiego endpointu.

---

`GET /tasks/?status=todo` — parametry query to **nie jest body**, więc nie używasz `json=`.
Używasz `params=`:

```python
# ŹLE — json to body requestu (POST/PUT)
client.get("/tasks/", json={"status": "todo"})

# DOBRZE — params to parametry URL
client.get("/tasks/", params={"status": "todo"})
# TestClient zamienia to na: GET /tasks/?status=todo
```

Możesz przekazać wiele parametrów naraz:

```python
client.get("/tasks/", params={"status": "todo", "priority": "high"})
# → GET /tasks/?status=todo&priority=high
```
