# Ściągawka: JWT w FastAPI

## 1. Po co JWT?

HTTP jest **bezstanowy** — serwer nie pamięta poprzednich żądań.
JWT rozwiązuje problem tożsamości: użytkownik **udowadnia kim jest** przy każdym żądaniu.

**Analogia:**
- Sesja (stara metoda) = szatnia: dostajesz numerek, portier sprawdza w księdze → baza przy każdym żądaniu
- JWT = paszport: masz dokument z danymi + pieczęcią, portier weryfikuje pieczęć bez dzwonienia do urzędu → baza tylko przy logowaniu

---

## 2. Struktura tokena JWT

Token to trzy części oddzielone kropką, zakodowane Base64:

```
xxxxx.yyyyy.zzzzz
  ^      ^      ^
header payload signature
```

### Header — algorytm szyfrowania
```json
{"alg": "HS256", "typ": "JWT"}
```

### Payload — dane użytkownika (claims)
```json
{
  "sub": "42",
  "email": "jan@example.com",
  "exp": 1710000000
}
```

### Signature — weryfikacja autentyczności
```
HMACSHA256(base64(header) + "." + base64(payload), SECRET_KEY)
```

> **WAŻNE:** JWT jest zakodowany Base64, NIE zaszyfrowany!
> Payload można odczytać bez klucza. Sekret służy tylko do weryfikacji podpisu.
> Nigdy nie wkładaj do payloadu haseł ani wrażliwych danych.

---

## 3. Przepływ autoryzacji

```
1. POST /auth/login  →  {username, password}
         ↓
2. Serwer sprawdza hasło w bazie (bcrypt.verify)
         ↓
3. Serwer tworzy JWT → zwraca {"access_token": "xxx", "token_type": "bearer"}
         ↓
4. Klient wysyła przy każdym żądaniu:
   Header: Authorization: Bearer xxx
         ↓
5. Serwer weryfikuje podpis → odczytuje user_id z "sub" → zwraca dane
```

---

## 4. Struktura plików

```
app/
  auth/
    __init__.py       ← pusty
    jwt.py            ← tworzenie i weryfikacja tokenów
    hashing.py        ← bcrypt: hash hasła + weryfikacja
    dependencies.py   ← get_current_user() do Depends()
  routers/
    auth.py           ← POST /auth/login + POST /auth/register
  schemas/
    auth.py           ← Token, TokenData
```

---

## 5. Paczki

```bash
pip install python-jose[cryptography]   # JWT encode/decode
pip install passlib[bcrypt]             # hashowanie haseł
pip install python-multipart            # OAuth2PasswordRequestForm support
```

---

## 6. Konfiguracja (.env)

```env
SECRET_KEY=twoj-bardzo-tajny-klucz-min-32-znaki
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Wczytywanie w kodzie:
```python
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
```

> `SECRET_KEY` nigdy nie trafia do repozytorium — dodaj `.env` do `.gitignore`!

---

## 7. Schematy Pydantic (schemas/auth.py)

```python
from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None
```

- `Token` — odpowiedź z endpointu logowania
- `TokenData` — dane wyciągnięte z payloadu tokena (wewnętrzne)

---

## 8. Hashowanie haseł (auth/hashing.py)

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

- `hash_password` — przy rejestracji, zapisujesz wynik do bazy
- `verify_password` — przy logowaniu, porównujesz z hashem z bazy
- bcrypt jest **celowo wolny** — utrudnia brute-force, to zaleta
- ten sam string daje **różne** hashe (salt jest losowy) — to normalne

---

## 9. Tworzenie i weryfikacja tokenów (auth/jwt.py)

```python
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from .config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
```

Wywołanie przy logowaniu:
```python
token = create_access_token(data={"sub": str(user.id)})
```

- `sub` (subject) — standardowy claim JWT, zazwyczaj user_id jako string
- `exp` — expiration, jose automatycznie weryfikuje przy dekodowaniu
- `jwt.decode()` rzuca `JWTError` gdy token nieważny lub wygasł

---

## 10. Dependency: get_current_user (auth/dependencies.py)

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.auth.jwt import decode_access_token
from app.schemas.auth import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == token_data.user_id).first()
    if user is None:
        raise credentials_exception
    return user
```

- `OAuth2PasswordBearer` — FastAPI helper, wyciąga token z headera `Authorization: Bearer`
- `tokenUrl` — URL gdzie klient może zdobyć token (dla Swagger UI)
- `Depends(oauth2_scheme)` — FastAPI automatycznie wyciąga token z każdego żądania
- funkcja zwraca obiekt `User` — gotowy do użycia w endpoincie

---

## 11. Router autoryzacji (routers/auth.py)

```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.auth.hashing import hash_password, verify_password
from app.auth.jwt import create_access_token
from app.schemas.auth import Token
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(user_data.password)
    user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
```

- `OAuth2PasswordRequestForm` — specjalny formularz OAuth2 (pola: `username`, `password`)
- FastAPI wymaga `python-multipart` żeby to działało
- `form_data.username` — mimo nazwy, wpisujemy tam email (standard OAuth2)

---

## 12. Chronione endpointy

```python
from fastapi import Depends
from app.auth.dependencies import get_current_user
from app.models import User

# Endpoint dostępny tylko dla zalogowanych
@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

# Endpoint gdzie użytkownik widzi tylko swoje projekty
@router.get("/projects/mine")
def get_my_projects(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Project).filter(Project.owner_id == current_user.id).all()
```

- `Depends(get_current_user)` — FastAPI wywołuje funkcję, wstrzykuje wynik
- jeśli token nieważny → automatycznie 401, endpoint się nie wykona
- `current_user` to pełny obiekt User z bazy

---

## 13. Zmiana modelu User

Model musi mieć `hashed_password` zamiast `password`:

```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)  # ← NOWE
    created_at = Column(DateTime, default=datetime.utcnow)
```

Schema `UserCreate` musi przyjmować `password` (plain text):
```python
class UserCreate(BaseModel):
    name: str
    email: str
    password: str   # ← plain text, hashujemy w routerze
```

Schema `UserResponse` NIE zwraca hasła:
```python
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

---

## 14. Podłączenie routera w main.py

```python
from app.routers.auth import router as auth_router

app.include_router(auth_router)
```

---

## 15. Zestawienie: kody statusów HTTP

| Sytuacja | Kod |
|---|---|
| Zły login/hasło | 401 Unauthorized |
| Brak tokena | 401 Unauthorized |
| Token wygasł | 401 Unauthorized |
| Próba dostępu do cudzych danych | 403 Forbidden |
| Email już zajęty | 400 Bad Request |
| Rejestracja OK | 201 Created |
| Login OK | 200 OK |

---

## 16. Przepływ end-to-end (podsumowanie)

```
Rejestracja:
POST /auth/register  →  hash(password)  →  User w bazie  →  UserResponse

Logowanie:
POST /auth/login  →  verify_password()  →  create_access_token()  →  Token

Chroniony endpoint:
GET /tasks/  +  Header: Authorization: Bearer xxx
  → oauth2_scheme wyciąga token
  → decode_access_token() weryfikuje podpis
  → get_current_user() pobiera usera z bazy
  → endpoint otrzymuje current_user
  → 200 OK z danymi
```

---

## 17. Pułapki i najczęstsze błędy

| Problem | Rozwiązanie |
|---|---|
| `422 Unprocessable Entity` na `/login` | Brak `python-multipart` — zainstaluj |
| `401` mimo dobrego hasła | Sprawdź czy `tokenUrl` w `oauth2_scheme` zgadza się z URL endpointu |
| `JWTError: Signature verification failed` | Zły `SECRET_KEY` — sprawdź `.env` |
| `AttributeError: hashed_password` | Model User nie ma tej kolumny — zaktualizuj + migracja bazy |
| Token nie wygasa | Nie dodajesz `exp` do payloadu — patrz `create_access_token` |
| Swagger nie daje przycisku "Authorize" | Brak `OAuth2PasswordBearer` w dependencies lub brak `tokenUrl` |
