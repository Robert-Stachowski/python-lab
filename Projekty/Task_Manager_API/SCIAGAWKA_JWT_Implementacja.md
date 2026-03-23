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

## 8. Co jeszcze zostało do zrobienia

Te cztery pliki to fundament. Żeby JWT działało w praktyce, potrzebne są jeszcze:

1. **`app/auth/dependencies.py`** — funkcja `get_current_user()` używana przez `Depends()`
2. **`app/routers/auth.py`** — endpointy `/auth/register` i `/auth/login`
3. **Zmiany w `app/models.py`** — kolumna `hashed_password` w modelu `User`
4. **Zmiany w `app/main.py`** — podłączenie nowego routera `auth`
5. **Dodanie `Depends(get_current_user)` do chronionych endpointów**
