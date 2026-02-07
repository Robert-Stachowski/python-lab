# 01 - Kontakty (Podstawowy CRUD)

## Trudnosc: ⭐ (Poczatkujacy)

## Cel
Przecwicz podstawowe operacje CRUD (Create, Read, Update, Delete) na pojedynczej tabeli.

## Baza danych
- **SQLite** (plik `contacts.db`)

## Model danych

### Contact (Kontakt)
| Kolumna | Typ | Ograniczenia |
|---------|-----|-------------|
| id | Integer | Primary Key, autoincrement |
| first_name | String(50) | NOT NULL |
| last_name | String(50) | NOT NULL |
| email | String(100) | NOT NULL, UNIQUE |
| phone | String(20) | opcjonalny |

## Zadania

### Zadanie 1: Konfiguracja
- Uzupelnij plik `.env` z DATABASE_URL dla SQLite
- Skonfiguruj polaczenie w `db.py`
- Zdefiniuj model `Contact` w `models.py`

### Zadanie 2: Create (Tworzenie)
- Dodaj co najmniej 5 kontaktow do bazy danych
- Upewnij sie, ze kazdy kontakt ma unikalne dane

### Zadanie 3: Read (Odczyt)
- Wyswietl wszystkie kontakty
- Znajdz kontakt po emailu
- Znajdz kontakty po nazwisku

### Zadanie 4: Update (Aktualizacja)
- Zmien numer telefonu wybranego kontaktu
- Zmien email wybranego kontaktu

### Zadanie 5: Delete (Usuwanie)
- Usun kontakt po ID
- Usun kontakt po emailu

## Podpowiedzi
- Uzyj `declarative_base()` do definicji modelu
- Uzyj `sessionmaker` i `create_engine` do polaczenia
- Pamietaj o `session.commit()` po kazdej zmianie
- Uzyj `session.query(Contact).filter_by(...)` do wyszukiwania
- Obsluz bledy za pomoca `try/except SQLAlchemyError`

## Przykladowy output
```
--- Wszystkie kontakty ---
1. Jan Kowalski | jan@email.com | 123-456-789
2. Anna Nowak | anna@email.com | 987-654-321
...

--- Szukam: jan@email.com ---
Znaleziono: Jan Kowalski

--- Aktualizacja telefonu ---
Jan Kowalski: nowy telefon -> 111-222-333

--- Usuwanie kontaktu ---
Usunieto: Anna Nowak
```
