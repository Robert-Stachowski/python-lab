# Ściągawka JWT — implementacja linijka po linijce

## Spis treści
1. Kontekst — co robimy i po co
2. Plik `app/config.py` — konfiguracja
3. Plik `app/auth/hashing.py` — hashowanie haseł
4. Plik `app/auth/jwt.py` — tworzenie i dekodowanie tokenów
5. Plik `app/schemas/auth.py` — schematy Pydantic
6. Przepływ danych przez wszystkie pliki
7. Najczęstsze błędy

---

## 1. Kontekst — co robimy i po co

Mamy API. Bez zabezpieczeń każdy może wywołać każdy endpoint.
JWT pozwala nam powiedzieć: "tylko zalogowany użytkownik może tutaj wejść".

Mechanizm w skrócie:
```
użytkownik loguje się → serwer sprawdza hasło → serwer daje token
użytkownik wysyła token przy każdym żądaniu → serwer sprawdza token → daje dostęp
```

Token to jak **bilet wstępu**. Dostajesz go przy wejściu (logowanie), pokazujesz przy każdej atrakcji (endpoint).

---

## 2. Plik `app/config.py` — konfiguracja

```python
import os                        # linia 1
from dotenv import load_dotenv   # linia 2
                                 # linia 3
load_dotenv()                    # linia 4
                                 # linia 5
SECRET_KEY = os.getenv("SECRET_KEY")           # linia 6
ALGORITHM = "HS256"                            # linia 7
ACCESS_TOKEN_EXPIRE_MINUTES = 30               # linia 8
```

### Linijka po linijce:

**linia 1: `import os`**
- Moduł standardowej biblioteki Pythona
- Daje dostęp do zmiennych środowiskowych systemu operacyjnego
- Używamy go do `os.getenv()` — odczyt zmiennej z `.env`

**linia 2: `from dotenv import load_dotenv`**
- `python-dotenv` to zewnętrzna paczka (była już zainstalowana wcześniej)
- `load_dotenv` to funkcja, która czyta plik `.env` i ładuje jego zawartość do pamięci

**linia 4: `load_dotenv()`**
- Wywołanie funkcji — bez tego `os.getenv()` nie znajdzie zmiennych z `.env`
- Musi być PRZED pierwszym `os.getenv()`
- Szuka pliku `.env` w katalogu projektu

**linia 6: `SECRET_KEY = os.getenv("SECRET_KEY")`**
- Czyta zmienną `SECRET_KEY` z pliku `.env`
- Jeśli jej nie ma — zwraca `None` (dlatego warto dodać walidację w produkcji)
- Ten klucz służy do **podpisywania tokenów** — kto go zna, może tworzyć fałszywe tokeny
- Dlatego nigdy nie trafia do repozytorium — jest tylko w `.env`

**linia 7: `ALGORITHM = "HS256"`**
- Algorytm podpisywania tokena
- `HS256` = HMAC + SHA-256 — symetryczny (ten sam klucz do tworzenia i weryfikacji)
- Inne opcje: `RS256` (asymetryczny — klucz prywatny/publiczny), ale `HS256` wystarczy na start
- Piszemy jako stała (WIELKIE LITERY) bo się nie zmienia podczas działania aplikacji

**linia 8: `ACCESS_TOKEN_EXPIRE_MINUTES = 30`**
- Token będzie ważny przez 30 minut
- Po tym czasie użytkownik dostanie 401 i musi się zalogować ponownie
- Krótki czas = większe bezpieczeństwo (skradziony token szybko wygasa)

### Po co osobny plik config.py?
Zamiast pisać `"HS256"` w kilku miejscach, piszemy raz tu i importujemy wszędzie.
Zmiana w jednym miejscu = zmiana wszędzie. Brak literówek.

---

## 3. Plik `app/auth/hashing.py` — hashowanie haseł

```python
from passlib.context import CryptContext    # linia 1
                                            # linia 2
                                            # linia 3
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")   # linia 4
                                            # linia 5
                                            # linia 6
def hash_password(password: str):           # linia 7
    return pwd_context.hash(password)       # linia 8
                                            # linia 9
                                            # linia 10
def verify_password(plain_password: str, hashed_password: str):     # linia 11
    return pwd_context.verify(plain_password, hashed_password)      # linia 12
```

### Linijka po linijce:

**linia 1: `from passlib.context import CryptContext`**
- `passlib` to zewnętrzna paczka do hashowania haseł
- `CryptContext` to klasa — "kontekst kryptograficzny", czyli obiekt który wie jak hashować
- Importujemy tylko tę jedną klasę, bo tylko jej potrzebujemy

**linia 4: `pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")`**
- Tworzymy jeden obiekt kontekstu — globalny dla całego pliku
- `schemes=["bcrypt"]` — używamy algorytmu bcrypt do hashowania
- `deprecated="auto"` — jeśli kiedyś zmienimy algorytm, stare hashe będą automatycznie oznaczone jako przestarzałe
- Ten obiekt tworzymy RAZ, nie w każdej funkcji (tworzenie jest kosztowne)

**Dlaczego bcrypt a nie SHA-256?**
SHA-256 jest błyskawiczny — atakujący może sprawdzać miliardy kombinacji na sekundę.
Bcrypt jest celowo wolny (setki ms) — brute-force staje się nieopłacalny.
Dodatkowo bcrypt dodaje losowy "salt" — dwa identyczne hasła dają różne hashe.

```
hash_password("kot123") → "$2b$12$abc...xyz"   (wynik 1)
hash_password("kot123") → "$2b$12$def...uvw"   (wynik 2)
```
Dlatego nie można porównać dwóch hashy — używamy `verify()`.

**linia 7-8: `def hash_password(password: str)`**
- Przyjmuje zwykłe hasło (tekst)
- `pwd_context.hash(password)` — zamienia go w hash bcrypt
- Zwraca string zaczynający się od `$2b$12$...`
- Używamy przy **rejestracji** — zapisujemy hash do bazy, nigdy oryginalne hasło

**linia 11-12: `def verify_password(plain_password, hashed_password)`**
- Przyjmuje DWA argumenty:
  - `plain_password` — hasło wpisane przez użytkownika (tekst)
  - `hashed_password` — hash zapisany w bazie danych
- `pwd_context.verify()` — sprawdza czy hasło pasuje do hasha
- Zwraca `True` lub `False`
- Używamy przy **logowaniu**

```
użytkownik wpisuje: "kot123"
baza danych ma:     "$2b$12$abc...xyz"
verify_password("kot123", "$2b$12$abc...xyz") → True
verify_password("pies123", "$2b$12$abc...xyz") → False
```

---

## 4. Plik `app/auth/jwt.py` — tworzenie i dekodowanie tokenów

```python
from datetime import timedelta, timezone, datetime           # linia 1
from jose import JWTError, jwt                               # linia 2
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES   # linia 3
                                                             # linia 4
                                                             # linia 5
def create_access_token(data: dict):                         # linia 8
    to_encode = data.copy()                                  # linia 9
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # linia 10
    to_encode.update({"exp": expire})                        # linia 11
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # linia 12
                                                             # linia 13
def decode_access_token(token: str):                         # linia 14
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])   # linia 15
```

### Linijka po linijce:

**linia 1: `from datetime import timedelta, timezone, datetime`**
- Importujemy trzy klasy z modułu `datetime`:
  - `datetime` — konkretny moment w czasie (np. "teraz": 2026-03-23 12:00:00)
  - `timedelta` — odcinek czasu (np. "30 minut", "2 godziny")
  - `timezone` — strefa czasowa (używamy `timezone.utc` — czas uniwersalny)
- Razem pozwalają obliczyć: "teraz + 30 minut = kiedy token wygasa"

**linia 2: `from jose import JWTError, jwt`**
- `python-jose` to zewnętrzna paczka do obsługi JWT
- `jwt` — moduł z funkcjami `encode()` i `decode()`
- `JWTError` — wyjątek rzucany gdy token jest nieprawidłowy (użyjemy go w `dependencies.py`)

**linia 3: `from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES`**
- Importujemy nasze stałe z `config.py`
- `app.config` — ścieżka absolutna (bo `config.py` jest w katalogu `app/`)
- Gdyby `config.py` był w tym samym katalogu (`auth/`), pisalibyśmy `from .config import ...`

---

### Funkcja `create_access_token`

**linia 8: `def create_access_token(data: dict):`**
- Przyjmuje słownik z danymi do zakodowania w tokenie
- Typowo wywołujemy ją tak: `create_access_token({"sub": str(user.id)})`
- `sub` (subject) — standardowe pole JWT oznaczające "o kim jest ten token"
- Dlaczego `str(user.id)`? Bo JWT przechowuje dane jako tekst

**linia 9: `to_encode = data.copy()`**
- Kopiujemy słownik — żeby nie modyfikować oryginału
- Bez `.copy()` — modyfikacja `to_encode` zmieniłaby też `data` (Python przekazuje referencję)
- To dobra praktyka defensywna

**linia 10: `expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)`**
- `datetime.now(timezone.utc)` — aktualny czas w strefie UTC (np. 12:00:00)
- `timedelta(minutes=30)` — kawałek czasu: 30 minut
- Wynik: konkretny moment wygaśnięcia (np. 12:30:00)
- Używamy UTC żeby uniknąć problemów ze strefami czasowymi — serwer może być w innym kraju niż użytkownik

**CZĘSTY BŁĄD:** `timedelta.now(...)` — to nie istnieje!
`now()` należy do klasy `datetime`, nie `timedelta`.
`timedelta` to tylko "kawałek czasu", nie ma pojęcia o "teraz".

**linia 11: `to_encode.update({"exp": expire})`**
- Dodajemy pole `exp` (expiration) do słownika
- `exp` to standardowe pole JWT — biblioteka `jose` automatycznie je sprawdza przy dekodowaniu
- Jeśli token wygasł → `jose` rzuca `JWTError`
- `.update()` to metoda słownika — dodaje/nadpisuje klucze

**linia 12: `return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)`**
- `jwt.encode()` — zamienia słownik w token JWT (string)
- Argumenty:
  - `to_encode` — dane do zakodowania (payload)
  - `SECRET_KEY` — tajny klucz do podpisania
  - `algorithm=ALGORITHM` — algorytm podpisywania
- Zwraca string np. `"eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI0MiJ9.abc123"`

---

### Funkcja `decode_access_token`

**linia 14: `def decode_access_token(token: str):`**
- Przyjmuje token (string) który przyszedł od użytkownika
- Używamy jej w `dependencies.py` przy weryfikacji każdego żądania

**linia 15: `return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])`**
- `jwt.decode()` — rozkodowuje token i zwraca słownik z danymi
- Argumenty:
  - `token` — string tokena od użytkownika
  - `SECRET_KEY` — ten sam klucz co przy kodowaniu
  - `algorithms=[ALGORITHM]` — lista algorytmów (lista, bo można akceptować kilka)
- Automatycznie sprawdza czy token nie wygasł (pole `exp`)
- Jeśli token nieprawidłowy lub wygasł → rzuca `JWTError`
- Zwraca słownik np. `{"sub": "42", "exp": 1710000000}`

**Dlaczego `algorithm=` (singular) przy encode, a `algorithms=` (plural) przy decode?**
Przy tworzeniu tokena używamy jednego konkretnego algorytmu.
Przy weryfikacji możemy akceptować kilka algorytmów (np. podczas migracji z HS256 na RS256).
To design biblioteki `jose` — trzeba zapamiętać.

---

## 5. Plik `app/schemas/auth.py` — schematy Pydantic

```python
from pydantic import BaseModel      # linia 1
from typing import Optional         # linia 2
                                    # linia 3
class Token(BaseModel):             # linia 4
    access_token: str               # linia 5
    token_type: str                 # linia 6
                                    # linia 7
class TokenData(BaseModel):         # linia 8
    user_id: Optional[int] = None   # linia 9
```

### Dwie klasy, dwa różne zastosowania:

**Klasa `Token`** — odpowiedź serwera po zalogowaniu

Gdy użytkownik się zaloguje, serwer zwraca:
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer"
}
```
- `access_token` — sam token JWT
- `token_type` — zawsze `"bearer"` (standard HTTP)
- Ta klasa definiuje **jak wygląda response** z endpointu `/auth/login`

**Klasa `TokenData`** — dane wyciągnięte z tokena

Gdy weryfikujemy token, dekodujemy go i wyciągamy `user_id`:
```python
payload = decode_access_token(token)
user_id = payload.get("sub")  # "42"
token_data = TokenData(user_id=int(user_id))
```
- `Optional[int] = None` — user_id może nie istnieć w payloadzie (obrona przed złym tokenem)
- Ta klasa definiuje **dane wewnętrzne** — nie jest bezpośrednio zwracana użytkownikowi
- Używamy jej w `dependencies.py` jako pomocniczą strukturę danych

### Dlaczego dwie osobne klasy a nie jedna?

`Token` = co serwer WYSYŁA do klienta (po zalogowaniu)
`TokenData` = co serwer WYCIĄGA z tokena (przy weryfikacji)

To dwa różne momenty, dwa różne kierunki przepływu danych.

---

## 6. Przepływ danych przez wszystkie pliki

### Rejestracja nowego użytkownika:
```
POST /auth/register
    → przyjmuje {email, password}
    → hashing.py: hash_password(password) → "$2b$12$..."
    → zapisuje do bazy: user.hashed_password = hash
    → zwraca dane użytkownika (bez hasła)
```

### Logowanie:
```
POST /auth/login
    → przyjmuje {email, password}
    → pobiera użytkownika z bazy po emailu
    → hashing.py: verify_password(password, user.hashed_password) → True/False
    → jeśli False: zwraca 401 Unauthorized
    → jeśli True:
        → jwt.py: create_access_token({"sub": str(user.id)}) → "eyJ..."
        → zwraca Token(access_token="eyJ...", token_type="bearer")
```

### Chroniony endpoint:
```
GET /tasks/
    → klient wysyła header: Authorization: Bearer eyJ...
    → FastAPI wyciąga token z headera (OAuth2PasswordBearer)
    → dependencies.py: get_current_user(token)
        → jwt.py: decode_access_token(token) → {"sub": "42", "exp": ...}
        → wyciąga user_id = 42
        → pobiera usera z bazy
        → zwraca obiekt User
    → endpoint dostaje current_user jako argument
    → zwraca dane
```

### Mapa importów:
```
config.py
    ↑
    imported by jwt.py

hashing.py ←── używany w routers/auth.py (rejestracja, logowanie)
jwt.py     ←── używany w auth/dependencies.py (weryfikacja tokena)
schemas/auth.py ←── używany w routers/auth.py (response_model=Token)
```

---

## 7. Najczęstsze błędy

| Błąd | Przyczyna | Rozwiązanie |
|---|---|---|
| `timedelta.now(...)` | `now()` to metoda `datetime`, nie `timedelta` | `datetime.now(timezone.utc)` |
| `algorithm=` vs `algorithms=` | `encode` przyjmuje string, `decode` przyjmuje listę | zapamiętać lub sprawdzić docs |
| `from .config import` nie działa | brak `__init__.py` w katalogu | utwórz pusty `app/auth/__init__.py` |
| Token zawsze `None` | `load_dotenv()` nie zostało wywołane | wywołaj `load_dotenv()` przed `os.getenv()` |
| `SECRET_KEY` w repozytorium | przypadkowe dodanie `.env` do git | dodaj `.env` do `.gitignore` |
| `sub` jako int zamiast string | JWT standard wymaga string | `str(user.id)` przy tworzeniu tokena |

---

## 8. Plik `app/auth/dependencies.py` — weryfikacja tokena przy każdym żądaniu

```python
from fastapi import Depends, HTTPException, status          # linia 1
from fastapi.security import OAuth2PasswordBearer           # linia 2
from jose import JWTError                                   # linia 3
from sqlalchemy.orm import Session                          # linia 4
from app.database import get_db                             # linia 5
from app.models import User                                 # linia 6
from app.auth.jwt import decode_access_token                # linia 7
from app.schemas.auth import TokenData                      # linia 8
                                                            # linia 9
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")  # linia 10
                                                            # linia 11
def get_current_user(                                       # linia 12
    token: str = Depends(oauth2_scheme),                    # linia 13
    db: Session = Depends(get_db)                           # linia 14
) -> User:                                                  # linia 15
    credentials_exception = HTTPException(                  # linia 16
        status_code=status.HTTP_401_UNAUTHORIZED,           # linia 17
        detail="Could not validate credentials",            # linia 18
        headers={"WWW-Authenticate": "Bearer"},             # linia 19
    )                                                       # linia 20
    try:                                                    # linia 21
        payload = decode_access_token(token)                # linia 22
        user_id_str = payload.get("sub")                    # linia 23
        if user_id_str is None:                             # linia 24
            raise credentials_exception                     # linia 25
        user_id = int(user_id_str)                          # linia 26
        token_data = TokenData(user_id=user_id)             # linia 27
    except JWTError:                                        # linia 28
        raise credentials_exception                         # linia 29
                                                            # linia 30
    user = db.query(User).filter(User.id == token_data.user_id).first()  # linia 31
    if user is None:                                        # linia 32
        raise credentials_exception                         # linia 33
    return user                                             # linia 34
```

### Linijka po linijce:

**linia 2: `from fastapi.security import OAuth2PasswordBearer`**
- Klasa FastAPI która automatycznie wyciąga token z headera HTTP
- Header musi wyglądać tak: `Authorization: Bearer eyJ...`
- Bez tego musielibyśmy ręcznie parsować każdy request

**linia 10: `oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")`**
- Tworzymy jeden globalny obiekt — używany jako `Depends(oauth2_scheme)`
- `tokenUrl="/auth/login"` — tylko dla Swagger UI: wie gdzie pokazać przycisk "Authorize"
- Nie ma wpływu na logikę weryfikacji tokena

**linia 12-15: `def get_current_user(...) -> User:`**
- Funkcja dependency — FastAPI wstrzykuje ją przez `Depends(get_current_user)`
- Przyjmuje dwa argumenty przez `Depends`:
  - `token` — string wyciągnięty z headera przez `oauth2_scheme`
  - `db` — sesja bazy danych
- Zwraca obiekt `User` — gotowy do użycia w endpoincie

**linia 16-20: `credentials_exception`**
- Definiujemy błąd raz, żeby nie powtarzać go w kilku miejscach
- `HTTP_401_UNAUTHORIZED` — "nie wiem kim jesteś"
- `headers={"WWW-Authenticate": "Bearer"}` — standard HTTP, informuje klienta jakiego typu autoryzacji oczekujemy

**linia 21-29: blok `try/except JWTError`**
- Owijamy dekodowanie w try/except — `decode_access_token()` rzuca `JWTError` gdy token jest zły lub wygasł
- Każdy błąd = 401, nie 500

**linia 23-26: bezpieczne wyciąganie user_id**
- `payload.get("sub")` — wyciągamy `sub` ze słownika (może być `None`)
- Sprawdzamy `None` PRZED `int()` — `int(None)` rzuciłby `ValueError`, nie `JWTError`
- Dopiero po sprawdzeniu konwertujemy na `int`

**linia 27: `token_data = TokenData(user_id=user_id)`**
- Pakujemy user_id w schemat Pydantic — dla porządku i bezpieczeństwa typów
- Nie jest wymagane, ale czytelniejsze niż przekazywanie gołego `int`

**linia 31-33: weryfikacja czy user nadal istnieje w bazie**
- Token może być ważny (dobry podpis, nie wygasł) ale user mógł zostać usunięty z bazy
- Dlatego zawsze sprawdzamy bazę — token sam w sobie nie wystarczy
- Jeśli brak usera → 401 (nie 404 — nie chcemy ujawniać czy user istnieje)

---

## 9. Plik `app/routers/auth.py` — endpointy rejestracji i logowania

```python
from fastapi import APIRouter, Depends, HTTPException, status     # linia 1
from fastapi.security import OAuth2PasswordRequestForm            # linia 2
from sqlalchemy.orm import Session                                # linia 3
from app.database import get_db                                   # linia 4
from app.models import User                                       # linia 5
from app.auth.hashing import hash_password, verify_password       # linia 6
from app.auth.jwt import create_access_token                      # linia 7
from app.schemas.auth import Token                                # linia 8
from app.schemas.user import UserCreate, UserResponse             # linia 9
                                                                  # linia 10
router = APIRouter(prefix="/auth", tags=["auth"])                 # linia 11
                                                                  # linia 12
@router.post("/register", response_model=UserResponse, status_code=201)  # linia 13
def register(user_data: UserCreate, db: Session = Depends(get_db)):      # linia 14
    existing = db.query(User).filter(User.username == user_data.username).first()  # linia 15
    if existing:                                                  # linia 16
        raise HTTPException(status_code=400, detail="Nazwa użytkownika jest już zajęta")  # linia 17
    existing = db.query(User).filter(User.email == user_data.email).first()  # linia 18
    if existing:                                                  # linia 19
        raise HTTPException(status_code=400, detail="Email jest już używany")  # linia 20
    hashed = hash_password(user_data.password)                    # linia 21
    user = User(                                                  # linia 22
        username=user_data.username,                              # linia 23
        email=user_data.email,                                    # linia 24
        hashed_password=hashed                                    # linia 25
    )                                                             # linia 26
    db.add(user)                                                  # linia 27
    db.commit()                                                   # linia 28
    db.refresh(user)                                              # linia 29
    return user                                                   # linia 30
                                                                  # linia 31
@router.post("/login", response_model=Token)                      # linia 32
def login(                                                        # linia 33
    form_data: OAuth2PasswordRequestForm = Depends(),             # linia 34
    db: Session = Depends(get_db)                                 # linia 35
):                                                                # linia 36
    user = db.query(User).filter(User.email == form_data.username).first()  # linia 37
    if not user or not verify_password(form_data.password, user.hashed_password):  # linia 38
        raise HTTPException(                                      # linia 39
            status_code=status.HTTP_401_UNAUTHORIZED,             # linia 40
            detail="Nieprawidłowy email lub hasło",               # linia 41
            headers={"WWW-Authenticate": "Bearer"},               # linia 42
        )                                                         # linia 43
    token = create_access_token(data={"sub": str(user.id)})       # linia 44
    return {"access_token": token, "token_type": "bearer"}        # linia 45
```

### Linijka po linijce:

**linia 2: `from fastapi.security import OAuth2PasswordRequestForm`**
- Specjalny formularz FastAPI dla standardu OAuth2
- Zamiast JSON (`{"email": ..., "password": ...}`) przyjmuje dane jako formularz HTML
- Dlatego wymagana jest paczka `python-multipart`
- Ma dwa pola: `username` i `password` — mimo nazwy `username` wpisujemy tam email

**linia 11: `router = APIRouter(prefix="/auth", tags=["auth"])`**
- `prefix="/auth"` — wszystkie endpointy zaczną się od `/auth`
- `/register` staje się `/auth/register`
- `/login` staje się `/auth/login`

**linia 15-20: podwójna walidacja unikalności**
- Sprawdzamy username i email osobno — żeby dać konkretny komunikat błędu
- Bez tego baza rzuciłaby `UNIQUE constraint failed` — brzydki błąd 500 zamiast 400
- Sprawdzamy przed zapisem, nie polegamy na constraintach bazy

**linia 21: `hashed = hash_password(user_data.password)`**
- `user_data.password` — plain text od użytkownika
- Nigdy nie zapisujemy plain text do bazy!
- `hash_password()` z `hashing.py` — zwraca hash bcrypt

**linia 22-25: tworzenie obiektu User**
- Jawnie podajemy pola zamiast `**user_data.model_dump()` — bo `model_dump()` zwróciłby `password` (plain text) zamiast `hashed_password`
- `hashed_password=hashed` — zapisujemy hash, nie oryginalne hasło

**linia 34: `form_data: OAuth2PasswordRequestForm = Depends()`**
- `Depends()` bez argumentu — FastAPI sam wie że to formularz OAuth2
- `form_data.username` — pole z emailem (OAuth2 standard nazywa to `username`)
- `form_data.password` — plain text hasło

**linia 37: szukanie po emailu**
- `form_data.username` zawiera email — taka jest konwencja OAuth2
- Szukamy usera po emailu, nie po username

**linia 38: podwójny warunek**
- `not user` — user nie istnieje w bazie
- `not verify_password(...)` — hasło się nie zgadza
- Oba dają ten sam błąd 401 — celowo! Nie chcemy ujawniać czy email istnieje w bazie

**linia 44: `create_access_token(data={"sub": str(user.id)})`**
- `sub` — user_id jako string (JWT standard)
- `str(user.id)` — konwersja bo JWT przechowuje dane jako tekst
- `create_access_token` dodaje automatycznie `exp` (czas wygaśnięcia)

---

## 10. Zmiany w `app/models.py` — kolumna hashed_password

```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(length=50), nullable=False, unique=True)
    email = Column(String(length=100), nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    hashed_password = Column(String, nullable=False)   # ← NOWE
```

- `hashed_password` — przechowujemy hash bcrypt, nigdy plain text
- `nullable=False` — każdy user MUSI mieć hasło (nie może być NULL)
- `String` bez długości — hash bcrypt ma stałą długość (~60 znaków), ale `String` bez limitu jest bezpieczniejszy

> **WAŻNE:** Jeśli baza już istnieje z użytkownikami bez `hashed_password`,
> dodanie `nullable=False` wymaga migracji lub usunięcia i recreacji tabel.

---

## 11. Zmiany w `app/main.py` — podłączenie routera auth

```python
from app.routers.auth import router as auth_router   # import z aliasem

app.include_router(auth_router)                      # podłączenie
```

- Import z aliasem `as auth_router` — bo zmienna nazywa się `router` w każdym pliku routera
- `include_router` BEZ prefixu — router `auth.py` już ma `prefix="/auth"` wewnątrz
- Kolejność ma znaczenie: `auth_router` podłączamy PRZED innymi routerami (konwencja)

---

## 12. Chronione endpointy — Depends(get_current_user)

```python
# W routers/users.py
from app.auth.dependencies import get_current_user
from app.models import User

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
```

```python
# W routers/projects.py
@router.get("/mine")
def get_my_projects(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Project).filter(Project.owner_id == current_user.id).all()
```

### Jak to działa:

**`Depends(get_current_user)`**
- FastAPI widzi `Depends` → wywołuje `get_current_user()` przed wykonaniem endpointu
- `get_current_user` wyciąga token, weryfikuje, pobiera usera z bazy
- Wynik (obiekt `User`) jest przekazany do endpointu jako `current_user`
- Jeśli token nieważny → 401, endpoint w ogóle się nie wykona

**`/me` — zwraca dane zalogowanego użytkownika**
- Nie potrzebuje `db` bo `current_user` już jest obiektem User z bazy
- Najprostszy chroniony endpoint — jeden `Depends`, jeden `return`

**`/mine` — filtruje zasoby po zalogowanym użytkowniku**
- Potrzebuje `db` żeby wykonać własne zapytanie
- `Project.owner_id == current_user.id` — filtr: tylko projekty tego usera
- `current_user.id` — id wyciągnięte z tokena, zweryfikowane w bazie

### Wzorzec do zapamiętania:
```
endpoint bez JWT  →  db: Session = Depends(get_db)
endpoint z JWT    →  current_user: User = Depends(get_current_user)
endpoint z JWT+db →  oba Depends naraz
```

---

## 13. Przepływ end-to-end (kompletny)

```
REJESTRACJA:
POST /auth/register {username, email, password}
    → auth.py: sprawdź unikalność username i email
    → hashing.py: hash_password(password) → "$2b$12$..."
    → zapisz User(username, email, hashed_password) do bazy
    → zwróć UserResponse (bez hasła)

LOGOWANIE:
POST /auth/login {username=email, password}
    → auth.py: znajdź usera po email
    → hashing.py: verify_password(password, hashed_password) → True/False
    → jeśli False: 401 Unauthorized
    → jeśli True: jwt.py: create_access_token({"sub": str(user.id)})
    → zwróć Token(access_token="eyJ...", token_type="bearer")

CHRONIONY ENDPOINT:
GET /users/me  +  Header: Authorization: Bearer eyJ...
    → oauth2_scheme wyciąga token z headera
    → dependencies.py: get_current_user(token)
        → jwt.py: decode_access_token(token) → {"sub": "42", "exp": ...}
        → sprawdź sub != None
        → user_id = int("42") = 42
        → pobierz User z bazy gdzie id=42
        → zwróć obiekt User
    → endpoint dostaje current_user
    → zwróć UserResponse
```
