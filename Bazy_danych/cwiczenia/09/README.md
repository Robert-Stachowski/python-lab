# 09 - System rezerwacji (Transakcje i walidacja)

## Trudnosc: ⭐⭐⭐⭐ (Zaawansowany)

## Cel
Przecwicz transakcje bazodanowe, rollback, walidacje danych i obsluge bledow.

## Baza danych
- **PostgreSQL** (wymaga serwera PostgreSQL)

## Model danych

### Room (Pokoj)
| Kolumna | Typ | Ograniczenia |
|---------|-----|-------------|
| id | Integer | Primary Key |
| name | String(100) | NOT NULL |
| capacity | Integer | NOT NULL |
| price_per_night | Float | NOT NULL |
| is_available | Boolean | default=True |

### Guest (Gosc)
| Kolumna | Typ | Ograniczenia |
|---------|-----|-------------|
| id | Integer | Primary Key |
| name | String(100) | NOT NULL |
| email | String(100) | NOT NULL, UNIQUE |
| phone | String(20) | opcjonalny |

### Reservation (Rezerwacja)
| Kolumna | Typ | Ograniczenia |
|---------|-----|-------------|
| id | Integer | Primary Key |
| guest_id | Integer | FK -> Guest.id |
| room_id | Integer | FK -> Room.id |
| check_in | Date | NOT NULL |
| check_out | Date | NOT NULL |
| total_price | Float | NOT NULL |
| status | String(20) | default="potwierdzona" |

### Relacje
- Guest -> Reservation: 1:N
- Room -> Reservation: 1:N

## Zadania

### Zadanie 1: Modele i seedowanie
- Zdefiniuj modele z relacjami
- Dodaj 5 pokojow o roznej pojemnosci i cenie
- Dodaj 4 gosci

### Zadanie 2: Tworzenie rezerwacji z walidacja
- Zaimplementuj funkcje `make_reservation()` ktora:
  - Sprawdza czy pokoj jest dostepny w podanym terminie
  - Sprawdza czy check_out > check_in
  - Oblicza laczna cene (ilosc nocy * cena za noc)
  - Tworzy rezerwacje w transakcji
  - W razie bledu robi rollback

### Zadanie 3: Sprawdzanie dostepnosci
- Zaimplementuj `check_availability(room_id, check_in, check_out)`:
  - Sprawdz czy pokoj nie ma kolidujacych rezerwacji
  - Kolizja = nowa rezerwacja naklada sie na istniejaca
- Wyswietl dostepne pokoje na dany termin

### Zadanie 4: Anulowanie rezerwacji
- Zaimplementuj `cancel_reservation()`:
  - Zmien status na "anulowana"
  - Cala operacja w transakcji
  - Jesli cos pojdzie nie tak -> rollback

### Zadanie 5: Raporty
- Lista aktywnych rezerwacji (status != "anulowana")
- Przychod z rezerwacji w danym miesiacu
- Pokoj z najwieksza liczba rezerwacji
- Gosc z najwieksza laczna kwota rezerwacji

## Podpowiedzi
- Kolizja dat: `and_(Reservation.check_in < new_check_out, Reservation.check_out > new_check_in)`
- Transakcja: `try: ... session.commit() except: session.rollback()`
- Liczba nocy: `(check_out - check_in).days`
- Status: uzyj stringa "potwierdzona", "anulowana", "zakonczona"
- `from sqlalchemy import and_, or_` do zlozonych warunkow

## Przykladowy output
```
--- Nowa rezerwacja ---
Sprawdzam dostepnosc pokoju "Deluxe" (15-20 stycznia)...
Pokoj dostepny! Cena: 5 nocy x 200 zl = 1000 zl
Rezerwacja #1 utworzona pomyslnie.

--- Kolizja! ---
Sprawdzam dostepnosc pokoju "Deluxe" (18-25 stycznia)...
BLAD: Pokoj zajety w terminie 15-20 stycznia!
Rezerwacja nie zostala utworzona.

--- Anulowanie ---
Rezerwacja #1 anulowana.

--- Raport ---
Aktywne rezerwacje: 3
Przychod w styczniu: 3500 zl
Najpopularniejszy pokoj: Deluxe (5 rezerwacji)
```
