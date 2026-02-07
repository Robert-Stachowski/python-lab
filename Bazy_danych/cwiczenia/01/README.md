# 01 - Kontakty (Podstawowy CRUD)

## TrudnoŚĆ: ⭐ (Początkujący)

## Cel
Przećwicz podstawowe operacje CRUD (Create, Read, Update, Delete) na pojedynczej tabeli.

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
- Uzupełnij plik `.env` z DATABASE_URL dla SQLite
- Skonfiguruj połączenie w `db.py`
- Zdefiniuj model `Contact` w `models.py`

### Zadanie 2: Create (Tworzenie)
- Dodaj co najmniej 5 kontaktów do bazy danych
- Upewnij się, że każdy kontakt ma unikalne dane

### Zadanie 3: Read (Odczyt)
- Wyświetl wszystkie kontakty
- Znajdź kontakt po emailu
- Znajdź kontakty po nazwisku

### Zadanie 4: Update (Aktualizacja)
- Zmień numer telefonu wybranego kontaktu
- Zmień email wybranego kontaktu

### Zadanie 5: Delete (Usuwanie)
- Usuń kontakt po ID
- Usuń kontakt po emailu

## Podpowiedzi
- Użyj `declarative_base()` do definicji modelu
- Użyj `sessionmaker` i `create_engine` do połączenia
- Pamietaj o `session.commit()` po każdej zmianie
- Użyj `session.query(Contact).filter_by(...)` do wyszukiwania
- Obsluz bledy za pomoca `try/except SQLAlchemyError`

## Przykładowy output
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
Usunięto: Anna Nowak
```
