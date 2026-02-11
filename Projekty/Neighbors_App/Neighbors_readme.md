# 🏘️ Sąsiedzi (Neighbors)

> Aplikacja do nawiązywania realnych, lokalnych kontaktów międzyludzkich — nie kolejny social media, a narzędzie do odzyskiwania bezpośredniego kontaktu z ludźmi wokół nas.

---

## 📌 Spis treści

- [Opis projektu](#-opis-projektu)
- [Problem, który rozwiązujemy](#-problem-który-rozwiązujemy)
- [Kluczowe funkcje](#-kluczowe-funkcje)
- [Stack technologiczny](#️-stack-technologiczny)
- [Mapa kompetencji](#-mapa-kompetencji)
- [Architektura systemu](#-architektura-systemu)
- [Modele danych](#-modele-danych)
- [Endpointy API](#-endpointy-api)
- [Plan realizacji](#-plan-realizacji)
- [Uruchomienie projektu](#-uruchomienie-projektu)
- [Testy](#-testy)
- [Bezpieczeństwo](#-bezpieczeństwo)
- [Potencjał rozwoju](#-potencjał-rozwoju)
- [Autor](#-autor)

---

## 📖 Opis projektu

**Sąsiedzi** to aplikacja webowa umożliwiająca użytkownikom lokalne spotkania z innymi osobami na podstawie ich aktualnych potrzeb lub statusów.

Przykładowe statusy:
- *„Chcę pogadać o wilczurach"*
- *„Piwo z kimś po pracy"*
- *„Potrzebuję się wygadać"*
- *„Chcę iść na spacer"*
- *„Potrzebuję pomocy przy przeprowadzce"*
- *„Zlecę drobną naprawę"*

**To nie jest portal randkowy.** Nacisk kładziony jest na **bezpieczeństwo**, **autentyczność** i **realne interakcje społeczne**.

---

## 🧩 Problem, który rozwiązujemy

Żyjemy w czasach, gdzie mimo tysięcy „znajomych" online, coraz trudniej nawiązać prawdziwy kontakt z osobą obok. Sąsiedzi odpowiada na pytanie:

> *„Czy ktoś w mojej okolicy ma teraz ochotę na to samo co ja?"*

Aplikacja łączy ludzi, którzy w danym momencie mają tę samą potrzebę — od zwykłej rozmowy po konkretną pomoc.

---

## 🔑 Kluczowe funkcje

### 🟢 MVP (po mentoringu — Django + znane technologie)
| Funkcja | Opis | Technologia |
|---|---|---|
| **Rejestracja i logowanie** | Email + hasło, system sesji | Django Auth (wbudowane) |
| **Profil użytkownika** | Imię, zdjęcie, krótki opis, miasto/dzielnica | Django models + DRF |
| **Statusy** | Użytkownik ustawia aktualny status (tekst + kategoria) | Django models + DRF |
| **Lista użytkowników w okolicy** | Filtrowanie po mieście/dzielnicy (bez mapy na start) | Django ORM filtering |
| **Prosty czat** | Wymiana wiadomości — polling HTTP | Django views + AJAX |
| **Panel admina** | Zarządzanie użytkownikami i statusami | Django Admin |

### 🟡 Faza 2 (samodzielna nauka — nowe technologie)
| Funkcja | Opis | Do nauki |
|---|---|---|
| **Geolokalizacja na mapie** | Mapa z użytkownikami w promieniu X km | GeoDjango + PostGIS + Leaflet |
| **JWT autentykacja** | Tokeny zamiast sesji (gotowość pod mobile) | django-allauth + Simple JWT |
| **Dokumentacja API** | Automatyczny Swagger / ReDoc | drf-spectacular |
| **Konteneryzacja** | Powtarzalne środowisko deweloperskie | Docker + docker-compose |
| **Deploy** | Aplikacja dostępna online | Railway / Fly.io |

### 🔴 Faza 3 (rozwój — zaawansowane funkcje)
| Funkcja | Opis | Do nauki |
|---|---|---|
| **Real-time czat** | WebSocket — wiadomości bez odświeżania | Django Channels + Redis |
| **Zadania w tle** | Wygaszanie statusów, powiadomienia email | Celery + Redis |
| **Weryfikacja tożsamości** | Zdjęcie dokumentu + selfie przez zewnętrzne API | Integracja z Sumsub / Veriff |
| **Oceny i profil zaufania** | Wzajemne ocenianie po spotkaniach | Django models |
| **Frontend mobilny** | Natywna aplikacja mobilna | Flutter / React Native |
| **System zgłoszeń** | Blokowanie, zgłoszenia, sygnał alarmowy | Django models + logika biznesowa |

---

## 🛠️ Stack technologiczny

### MVP (to, co znam po mentoringu)
```
Python 3.12 + Django 5.x + Django REST Framework
PostgreSQL (standardowy, bez PostGIS)
Django Auth (wbudowany system sesji)
Django Admin
pytest / unittest
Git + GitHub
```

### Docelowy stack (do nauki po MVP)
```
GeoDjango + PostGIS .............. geolokalizacja na mapie
Docker + docker-compose .......... konteneryzacja
Redis ............................ cache, broker wiadomości
Celery ........................... zadania asynchroniczne
Django Channels .................. WebSocket (real-time czat)
django-allauth + Simple JWT ...... zaawansowana autentykacja
drf-spectacular .................. dokumentacja API (Swagger)
Leaflet / Google Maps API ........ mapa w przeglądarce
Railway / Fly.io ................. deploy
React / Flutter .................. frontend (opcjonalnie)
```

---

## 🗺 Mapa kompetencji

Przejrzysty podział na to, co potrafię teraz, a czego się douczę:

```
✅ UMIEM (po mentoringu)          📚 DO NAUKI (samodzielnie)
─────────────────────────         ──────────────────────────
Python                            GeoDjango + PostGIS
Django (views, models, ORM)       Docker + docker-compose
Django REST Framework             Redis + Celery
PostgreSQL (podstawowy)           Django Channels (WebSocket)
Django Admin                      django-allauth + JWT
Django Auth (sesje)               drf-spectacular (Swagger)
Testy (pytest)                    Leaflet / Google Maps API
Git + GitHub                      Deploy (Railway / Fly.io)
                                  Integracja KYC (Sumsub)
                                  Frontend (React / Flutter)
```

> **Strategia**: Buduję MVP na tym, co znam. Każda nowa technologia to osobna iteracja — uczę się i dodaję do projektu krok po kroku.

---

## 🏗 Architektura systemu

### MVP (prosta architektura)
```
┌──────────────────────────────────┐
│          PRZEGLĄDARKA            │
│    (Django templates / DRF)      │
└───────────────┬──────────────────┘
                │ HTTP
                ▼
┌──────────────────────────────────┐
│          DJANGO + DRF            │
│                                  │
│  ┌──────────┐  ┌──────────────┐  │
│  │   Auth   │  │   Profiles   │  │
│  │ (sesje)  │  │ (miasto/dz.) │  │
│  └──────────┘  └──────────────┘  │
│  ┌──────────┐  ┌──────────────┐  │
│  │ Statuses │  │     Chat     │  │
│  │  (CRUD)  │  │  (polling)   │  │
│  └──────────┘  └──────────────┘  │
└───────────────┬──────────────────┘
                │
                ▼
        ┌──────────────┐
        │  PostgreSQL   │
        └──────────────┘
```

### Docelowa architektura (po rozbudowie)
```
┌─────────────────────────────────────────────────────────┐
│                       KLIENT                            │
│         (React / Flutter / Swagger UI / Leaflet)        │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTPS (REST API + WebSocket)
                       ▼
┌─────────────────────────────────────────────────────────┐
│                   DJANGO + DRF                          │
│                                                         │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │  Auth (JWT) │  │   Profiles   │  │   Statuses    │  │
│  │  (allauth)  │  │  (GeoDjango) │  │  (CRUD+Geo)   │  │
│  └─────────────┘  └──────────────┘  └───────────────┘  │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │    Chat     │  │   Ratings    │  │   Reports     │  │
│  │ (Channels)  │  │              │  │               │  │
│  └─────────────┘  └──────────────┘  └───────────────┘  │
└──────────┬───────────────┬──────────────┬───────────────┘
           │               │              │
           ▼               ▼              ▼
    ┌────────────┐  ┌────────────┐  ┌────────────┐
    │ PostgreSQL │  │   Redis    │  │   Celery   │
    │  + PostGIS │  │            │  │  (worker)  │
    └────────────┘  └────────────┘  └────────────┘
                                          │
                                          ▼
                                   ┌────────────┐
                                   │ Zewnętrzne  │
                                   │ API (KYC,   │
                                   │ Maps, FCM)  │
                                   └────────────┘
```

---

## 🗃 Modele danych

### UserProfile (MVP)
```python
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=50)
    bio = models.TextField(max_length=300, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    city = models.CharField(max_length=100)                    # MVP: tekst
    district = models.CharField(max_length=100, blank=True)    # MVP: tekst
    # location = models.PointField(geography=True)             # Faza 2: GeoDjango
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.display_name
```

### Status (MVP)
```python
class Status(models.Model):
    class Category(models.TextChoices):
        TALK = 'talk', 'Pogadajmy'
        ACTIVITY = 'activity', 'Wspólna aktywność'
        HELP = 'help', 'Potrzebuję pomocy'
        OFFER = 'offer', 'Oferuję pomoc'
        EVENT = 'event', 'Wydarzenie'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='statuses')
    text = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=Category.choices)
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.text}"
```

### ChatMessage (MVP)
```python
class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField(max_length=1000)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender} → {self.receiver}: {self.content[:50]}"
```

---

## 🔌 Endpointy API

### MVP — Autentykacja (Django Auth + sesje)
| Metoda | Endpoint | Opis |
|--------|----------|------|
| POST | `/api/auth/register/` | Rejestracja nowego użytkownika |
| POST | `/api/auth/login/` | Logowanie (sesja) |
| POST | `/api/auth/logout/` | Wylogowanie |

### MVP — Profil
| Metoda | Endpoint | Opis |
|--------|----------|------|
| GET | `/api/profiles/me/` | Pobranie własnego profilu |
| PATCH | `/api/profiles/me/` | Aktualizacja profilu (miasto, dzielnica, bio) |
| GET | `/api/profiles/<id>/` | Podgląd profilu innego użytkownika |

### MVP — Statusy
| Metoda | Endpoint | Opis |
|--------|----------|------|
| GET | `/api/statuses/` | Lista aktywnych statusów (filtr: kategoria, miasto) |
| POST | `/api/statuses/` | Utworzenie nowego statusu |
| PATCH | `/api/statuses/<id>/` | Edycja własnego statusu |
| DELETE | `/api/statuses/<id>/` | Usunięcie własnego statusu |

### MVP — Czat
| Metoda | Endpoint | Opis |
|--------|----------|------|
| GET | `/api/chats/` | Lista konwersacji użytkownika |
| GET | `/api/chats/<user_id>/messages/` | Wiadomości z danym użytkownikiem |
| POST | `/api/chats/<user_id>/messages/` | Wysłanie wiadomości |

### Faza 2+ (po nauce nowych technologii)
| Metoda | Endpoint | Opis |
|--------|----------|------|
| GET | `/api/statuses/nearby/?lat=X&lng=Y&radius=5` | Statusy w promieniu (GeoDjango) |
| POST | `/api/auth/token/` | JWT token (allauth) |
| POST | `/api/auth/token/refresh/` | Odświeżenie JWT |
| POST | `/api/ratings/` | Wystawienie oceny po spotkaniu |
| GET | `/api/ratings/<user_id>/` | Oceny danego użytkownika |
| GET | `/api/docs/` | Swagger UI (drf-spectacular) |

---

## 📅 Plan realizacji

### 🟢 Etap 1: MVP (po mentoringu — znane technologie)

**Tydzień 1–2: Fundament**
- [ ] Inicjalizacja projektu Django + DRF
- [ ] Konfiguracja PostgreSQL (standardowy)
- [ ] Model `UserProfile` z polami `city` i `district`
- [ ] Rejestracja i logowanie (Django Auth — sesje)
- [ ] Endpoint `/api/profiles/me/`
- [ ] Pierwsze testy

**Tydzień 3–4: Statusy i filtrowanie**
- [ ] Model `Status` z kategoriami
- [ ] CRUD endpointy dla statusów
- [ ] Filtrowanie statusów po mieście i kategorii
- [ ] Automatyczne wygaszanie statusów (management command)
- [ ] Testy endpointów

**Tydzień 5–6: Czat i interakcje**
- [ ] Model `ChatMessage`
- [ ] Endpointy czatu (HTTP polling)
- [ ] Paginacja wiadomości
- [ ] Walidacja i uprawnienia (DRF permissions)
- [ ] Testy czatu

**Tydzień 7–8: Polish**
- [ ] Porządki w kodzie i refaktoring
- [ ] Kompletne testy (coverage > 80%)
- [ ] README z instrukcją uruchomienia
- [ ] Deploy na PythonAnywhere (darmowy, prosty — na start)

---

### 🟡 Etap 2: Nauka i rozbudowa (samodzielnie, po MVP)

Każdy punkt to osobna „iteracja nauki" — uczę się technologii i wdrażam ją w projekcie.

**Iteracja 2.1 — Docker**
- [ ] 📚 Nauka: Docker, docker-compose, Dockerfile
- [ ] Konteneryzacja projektu (django + postgres)
- [ ] Plik `docker-compose.yml`
- [ ] Aktualizacja README z instrukcją Docker

**Iteracja 2.2 — GeoDjango + PostGIS**
- [ ] 📚 Nauka: PostGIS, GeoDjango, PointField, zapytania geoprzestrzenne
- [ ] Migracja `city/district` → `PointField` w profilu i statusach
- [ ] Endpoint `/api/statuses/nearby/` z filtrowaniem po promieniu
- [ ] Dodanie PostGIS do docker-compose

**Iteracja 2.3 — Mapa (Leaflet)**
- [ ] 📚 Nauka: Leaflet.js (podstawy frontendu)
- [ ] Prosta strona HTML z mapą pokazującą statusy w okolicy
- [ ] Integracja z endpointem nearby

**Iteracja 2.4 — JWT + allauth**
- [ ] 📚 Nauka: django-allauth, dj-rest-auth, Simple JWT
- [ ] Migracja z sesji na JWT
- [ ] Obsługa OAuth (Google login)
- [ ] Token refresh endpoint

**Iteracja 2.5 — Dokumentacja API**
- [ ] 📚 Nauka: drf-spectacular
- [ ] Swagger UI pod `/api/docs/`
- [ ] ReDoc pod `/api/redoc/`

**Iteracja 2.6 — Deploy (produkcyjny)**
- [ ] 📚 Nauka: Railway / Fly.io, zmienne środowiskowe, Gunicorn
- [ ] CI/CD pipeline (GitHub Actions: lint + testy)
- [ ] Deploy aplikacji z Dockerem

---

### 🔴 Etap 3: Zaawansowane funkcje (dalszy rozwój)

**Iteracja 3.1 — Redis + Celery**
- [ ] 📚 Nauka: Redis, Celery, task queue
- [ ] Redis jako broker do docker-compose
- [ ] Celery task: automatyczne wygaszanie statusów
- [ ] Celery task: powiadomienia email

**Iteracja 3.2 — Real-time czat**
- [ ] 📚 Nauka: Django Channels, WebSocket, ASGI
- [ ] Migracja czatu z pollingu na WebSocket
- [ ] Redis jako channel layer

**Iteracja 3.3 — System ocen i zaufania**
- [ ] Model `Rating` (ocena + komentarz)
- [ ] Logika obliczania `trust_score`
- [ ] Odznaki i profil zaufania

**Iteracja 3.4 — KYC (weryfikacja tożsamości)**
- [ ] 📚 Nauka: API Sumsub/Veriff, webhooks
- [ ] Mock integracji w środowisku dev
- [ ] Endpoint do inicjowania weryfikacji

**Iteracja 3.5 — Frontend mobilny**
- [ ] 📚 Nauka: Flutter lub React Native
- [ ] Aplikacja mobilna konsumująca istniejące API

---

## 🚀 Uruchomienie projektu

### MVP (bez Dockera)
```bash
# Sklonuj repozytorium
git clone https://github.com/TWOJ_USERNAME/sasiedzi.git
cd sasiedzi

# Utwórz i aktywuj wirtualne środowisko
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Zainstaluj zależności
pip install -r requirements.txt

# Skonfiguruj zmienne środowiskowe
cp .env.example .env
# Edytuj .env — ustaw DATABASE_URL, SECRET_KEY

# Migracje i uruchomienie
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# Aplikacja dostępna pod:
# API:   http://localhost:8000/api/
# Admin: http://localhost:8000/admin/
```

### Po Etapie 2 (z Dockerem)
```bash
# Skopiuj zmienne środowiskowe
cp .env.example .env

# Uruchom kontenery
docker-compose up --build

# Migracje
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

# Aplikacja dostępna pod:
# API:     http://localhost:8000/api/
# Swagger: http://localhost:8000/api/docs/
# Admin:   http://localhost:8000/admin/
```

---

## 🧪 Testy

```bash
# Uruchomienie wszystkich testów
pytest

# Z pokryciem kodu
pytest --cov=apps --cov-report=html

# Tylko testy statusów
pytest apps/statuses/tests/ -v
```

### Co jest testowane (MVP):
- Rejestracja, logowanie, wylogowanie
- CRUD statusów (tworzenie, edycja, usuwanie)
- Filtrowanie statusów po mieście i kategorii
- Uprawnienia (dostęp do cudzych danych, edycja tylko swoich)
- Czat — wysyłanie i pobieranie wiadomości
- Walidacja danych wejściowych
- Edge cases (wygasłe statusy, puste pola)

---

## 🔐 Bezpieczeństwo

### MVP
| Warstwa | Rozwiązanie |
|---------|------------|
| Autentykacja | Django Auth (sesje) |
| Autoryzacja | DRF permissions (IsAuthenticated, IsOwner) |
| Walidacja | Serializery DRF + walidacja modeli |
| Zmienne środowiskowe | python-decouple, brak sekretów w kodzie |
| CSRF | Django middleware (wbudowane) |

### Docelowo (Etap 2+)
| Warstwa | Rozwiązanie |
|---------|------------|
| Autentykacja | JWT (access + refresh tokens) |
| KYC | Zewnętrzny dostawca — dane nie trafiają na serwer |
| Rate limiting | DRF throttling |
| CORS | django-cors-headers z whitelistą |
| Szyfrowanie | HTTPS + szyfrowanie danych wrażliwych |

---

## 🌱 Potencjał rozwoju

```
MVP (Django + DRF + PostgreSQL)
 │
 ├── + Docker ─────────────── profesjonalne środowisko
 ├── + GeoDjango + Leaflet ── mapa z lokalizacją
 ├── + JWT + allauth ──────── gotowość pod mobile
 ├── + Swagger ────────────── dokumentacja API
 ├── + Deploy ─────────────── aplikacja online
 │
 ├── + Redis + Celery ─────── zadania w tle
 ├── + Django Channels ────── real-time czat
 ├── + System ocen ────────── profil zaufania
 ├── + KYC ────────────────── weryfikacja tożsamości
 │
 └── + Frontend mobilny ───── Flutter / React Native
      ├── Społeczności lokalne
      ├── Wspólne wydarzenia
      └── Integracja z NGO / samorządem
```

---

## 👤 Autor

**Robert Stachowski**

Projekt realizowany jako końcowy projekt ścieżki nauki Python / Django Developer.
Każda faza projektu odpowiada kolejnemu etapowi nauki — od MVP po zaawansowane technologie.

- GitHub: [https://github.com/Robert-Stachowski](https://github.com/Robert-Stachowski)
- LinkedIn: [https://www.linkedin.com/in/robert-stachowski/](https://www.linkedin.com/in/robert-stachowski-3a9aa2365/)
- Email: Robert.Stachowski.dev@gmail.com

---

## 📄 Licencja

Ten projekt jest udostępniony na licencji MIT — szczegóły w pliku [LICENSE](LICENSE).
