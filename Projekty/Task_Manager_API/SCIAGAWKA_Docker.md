# Ściągawka: Docker + docker-compose dla FastAPI

---

## 1. Po co w ogóle Docker?

Wyobraź sobie, że piszesz aplikację i mówisz znajomemu: "u mnie działa". On odpala na swoim komputerze — nie działa. Dlaczego? Bo ma inną wersję Pythona. Inne paczki. Inny system operacyjny.

Docker rozwiązuje ten problem raz na zawsze.

**Idea:** zamiast mówić "zainstaluj Pythona 3.12, zainstaluj te paczki, ustaw te zmienne środowiskowe..." — pakujesz **całe środowisko** razem z aplikacją do jednego pudełka. Pudełko działa tak samo wszędzie.

To pudełko nazywa się **kontener**.

---

## 2. Kluczowe pojęcia — od podstaw

### Image (obraz)
To **przepis** na kontener. Opisuje: jaki system, jaka wersja Pythona, jakie paczki, jakie pliki. Sam w sobie nie działa — to tylko szablon.

Analogia: **klasa w Pythonie** — definiuje jak coś ma wyglądać, ale jeszcze nie istnieje jako obiekt.

### Kontener
To **uruchomiony image** — żywa instancja. Możesz mieć 10 kontenerów z jednego image, tak jak możesz mieć 10 obiektów z jednej klasy.

Analogia: **obiekt klasy** — konkretna, działająca rzecz.

### Dockerfile
To plik tekstowy z instrukcjami **jak zbudować image**. Piszesz w nim krok po kroku: weź Pythona 3.12, skopiuj moje pliki, zainstaluj paczki, uruchom serwer.

Analogia: **instrukcja IKEA** — krok po kroku jak złożyć mebel.

### docker-compose
Narzędzie do uruchamiania **wielu kontenerów naraz**. Nasza aplikacja potrzebuje dwóch rzeczy: FastAPI i PostgreSQL. `docker-compose` uruchamia oba, łączy je w sieć i sprawia, że gadają ze sobą.

Analogia: **dyrygent orkiestry** (więcej o tym poniżej).

### Volume (wolumin)
Folder współdzielony między Twoim komputerem a kontenerem. Przydatny np. żeby dane z bazy danych nie znikały po restarcie kontenera.

Analogia: **pendrive** podpięty do kontenera — dane są na zewnątrz, kontener może się zrestartować, a dane zostają.

---

## 3. Orchestracja — co to znaczy?

Słowo brzmi groźnie, ale idea jest prosta.

**Orkiestra** ma 50 muzyków. Każdy gra swój instrument. Bez dyrygenta każdy zaczyna kiedy chce, gra w swoim tempie — chaos. Dyrygent mówi: "najpierw wchodzą skrzypce, potem trąbki, wszyscy grają w tym samym tempie, jeśli ktoś się zgubi — czekamy".

W świecie Dockera:
- Każdy **serwis** (FastAPI, PostgreSQL, Redis, cokolwiek) to jeden muzyk
- **docker-compose** to dyrygent — mówi w jakiej kolejności uruchamiać serwisy, jak je połączyć, co zrobić gdy któryś padnie

Konkretnie w naszym projekcie:
- PostgreSQL musi **wystartować przed** FastAPI (bo FastAPI od razu próbuje się połączyć z bazą)
- docker-compose wie o tej zależności i pilnuje kolejności
- Oba serwisy dostają wspólną sieć — FastAPI może "ping-ować" PostgreSQL po nazwie `db`, nie po IP

---

## 4. Jak wygląda nasz projekt z Dockerem

```
Task_Manager_API/
  app/
  tests/
  Dockerfile          ← jak zbudować obraz FastAPI
  docker-compose.yml  ← jak uruchomić FastAPI + PostgreSQL razem
  .env                ← hasła i klucze (nigdy w repozytorium!)
  requirements.txt    ← lista paczek (Docker ją użyje)
```

---

## 5. Dockerfile — linijka po linijce

```dockerfile
FROM python:3.12-slim
```
"Zacznij od oficjalnego obrazu Pythona 3.12 w wersji slim (odchudzona — mniej MB)."
To jak `import` — nie piszesz Pythona od zera, bierzesz gotowy.

```dockerfile
WORKDIR /app
```
"Ustaw katalog roboczy wewnątrz kontenera na `/app`."
Wszystkie następne komendy będą wykonywane w tym katalogu.

```dockerfile
COPY requirements.txt .
```
"Skopiuj plik `requirements.txt` z Twojego komputera do kontenera (do `/app/`)."
Robimy to **przed** kopiowaniem reszty kodu — zaraz zobaczysz dlaczego.

```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```
"Zainstaluj wszystkie paczki z requirements.txt."
`--no-cache-dir` — nie zapisuj cache pip-a, żeby obraz był lżejszy.

```dockerfile
COPY . .
```
"Skopiuj cały projekt (`.`) do kontenera (`.` = `/app/`)."
Dlaczego dopiero teraz? Docker **cache'uje warstwy** — jeśli `requirements.txt` się nie zmienił, nie instaluje paczek od nowa przy każdej zmianie kodu. Sprytna optymalizacja.

```dockerfile
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```
"Gdy kontener startuje — uruchom serwer uvicorn."
`--host 0.0.0.0` — nasłuchuj na wszystkich interfejsach sieciowych (bez tego kontener byłby niedostępny z zewnątrz).

---

## 6. docker-compose.yml — linijka po linijce

```yaml
version: "3.9"
```
Wersja składni docker-compose. Traktuj jak `# Python 3.12` na górze pliku.

```yaml
services:
```
Tutaj definiujesz wszystkie serwisy (kontenery) które chcesz uruchomić.

```yaml
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: taskmanager
    volumes:
      - postgres_data:/var/lib/postgresql/data
```
Serwis `db`:
- `image: postgres:15` — użyj gotowego obrazu PostgreSQL 15 (nie piszemy Dockerfile dla bazy)
- `environment` — zmienne środowiskowe dla PostgreSQL (nazwa bazy, user, hasło)
- `volumes` — dane bazy zapisuj w woluminie `postgres_data`, nie wewnątrz kontenera (żeby nie znikały po restarcie)

```yaml
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db:5432/taskmanager
    depends_on:
      - db
```
Serwis `web` (nasza FastAPI):
- `build: .` — zbuduj obraz z `Dockerfile` w bieżącym katalogu
- `ports: "8000:8000"` — przekaż port 8000 kontenera na port 8000 Twojego komputera (format: `host:kontener`)
- `environment` — zmienna DATABASE_URL dla naszej aplikacji. Zamiast `localhost` piszemy `db` — to nazwa serwisu w docker-compose, działa jak DNS
- `depends_on: db` — "uruchom mnie dopiero po starcie serwisu db"

```yaml
volumes:
  postgres_data:
```
Deklaracja woluminu `postgres_data`. Docker zarządza nim samodzielnie.

---

## 7. Połączenie z bazą danych — kluczowa zmiana

Bez Dockera w `.env` masz:
```
DATABASE_URL=postgresql://postgres:haslo@localhost:5432/taskmanager
```

Z Dockerem `localhost` **nie działa** — FastAPI i PostgreSQL są w osobnych kontenerach. Zamiast `localhost` używasz **nazwy serwisu** z docker-compose:
```
DATABASE_URL=postgresql://postgres:postgres@db:5432/taskmanager
```

`db` to nazwa serwisu zdefiniowana w `docker-compose.yml`. Docker sam rozwiązuje ten adres do właściwego kontenera.

---

## 8. Podstawowe komendy

```bash
# Zbuduj obrazy i uruchom wszystkie serwisy
docker-compose up --build

# Uruchom w tle (detached)
docker-compose up --build -d

# Zatrzymaj wszystko
docker-compose down

# Zatrzymaj i usuń woluminy (dane bazy!)
docker-compose down -v

# Zobacz logi
docker-compose logs web
docker-compose logs db

# Wejdź do kontenera (terminal wewnątrz)
docker-compose exec web bash
```

---

## 9. Przepływ — co się dzieje po `docker-compose up --build`

```
1. Docker czyta docker-compose.yml
2. Buduje obraz "web" z Dockerfile (instaluje paczki, kopiuje kod)
3. Pobiera gotowy obraz "postgres:15" z Docker Hub
4. Uruchamia kontener "db" (PostgreSQL)
5. Czeka aż "db" wystartuje (depends_on)
6. Uruchamia kontener "web" (FastAPI)
7. FastAPI łączy się z bazą przez adres "db:5432"
8. Aplikacja dostępna na http://localhost:8000
```

---

## 10. .dockerignore — czego nie kopiować do obrazu

Tak jak `.gitignore` mówi gitowi co ignorować, `.dockerignore` mówi Dockerowi co **nie** kopiować do obrazu:

```
.venv
__pycache__
*.pyc
.env
.git
```

Po co? `COPY . .` skopiowałoby też `.venv` (setki MB) i `.env` (hasła!) do obrazu. `.dockerignore` temu zapobiega.

---

## 11. Zestawienie — co tworzysz

| Plik | Gdzie | Po co |
|---|---|---|
| `Dockerfile` | główny katalog | przepis na obraz FastAPI |
| `docker-compose.yml` | główny katalog | orchestracja FastAPI + PostgreSQL |
| `.dockerignore` | główny katalog | co nie trafia do obrazu |
| `.env` | główny katalog | zmienne środowiskowe (już masz) |

---

## 12. Najczęstsze pułapki dla początkujących

| Pułapka | Rozwiązanie |
|---|---|
| `localhost` w DATABASE_URL | Zmień na nazwę serwisu: `db` |
| Dane bazy znikają po restarcie | Użyj `volumes` |
| `.env` trafia do obrazu | Dodaj do `.dockerignore` |
| `uvicorn` niedostępny z zewnątrz | `--host 0.0.0.0` w CMD |
| FastAPI startuje przed bazą | `depends_on: db` w docker-compose |
| Zmiany w kodzie nie widoczne | Przebuduj: `docker-compose up --build` |
