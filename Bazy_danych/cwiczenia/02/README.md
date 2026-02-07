# 02 - Dziennik treningow (Filtrowanie i sortowanie)

## Trudnosc: (Poczatkujacy)

## Cel
Przecwicz filtrowanie, sortowanie i wyszukiwanie danych w pojedynczej tabeli.

## Baza danych
- **SQLite** (plik `workouts.db`)

## Model danych

### Workout (Trening)
| Kolumna | Typ | Ograniczenia |
|---------|-----|-------------|
| id | Integer | Primary Key, autoincrement |
| name | String(100) | NOT NULL |
| workout_type | String(50) | NOT NULL (np. "cardio", "sila", "rozciaganie") |
| duration_minutes | Integer | NOT NULL |
| calories | Integer | opcjonalny |
| date | Date | NOT NULL, default=dzis |

## Zadania

### Zadanie 1: Konfiguracja i seedowanie
- Skonfiguruj polaczenie z baza danych
- Zdefiniuj model `Workout`
- Dodaj co najmniej 10 treningow roznych typow i z roznymi datami

### Zadanie 2: Filtrowanie
- Znajdz wszystkie treningi typu "cardio"
- Znajdz treningi dluzsze niz 30 minut
- Znajdz treningi z ostatnich 7 dni

### Zadanie 3: Sortowanie
- Wyswietl treningi posortowane po dacie (od najnowszego)
- Wyswietl treningi posortowane po spalonych kaloriach (malejaco)
- Wyswietl treningi posortowane po czasie trwania (rosnaco)

### Zadanie 4: Laczenie filtrow
- Znajdz treningi typu "sila" dluzsze niz 45 minut, posortowane po dacie
- Znajdz 3 najdluzsze treningi cardio

## Podpowiedzi
- Uzyj `filter()` z operatorami: `==`, `>`, `<`, `>=`
- Do filtrowania dat uzyj `datetime.date.today()` i `timedelta`
- `order_by(Workout.date.desc())` sortuje malejaco
- Mozesz laczyc filtry: `session.query(...).filter(...).filter(...)`
- `limit(3)` ogranicza wyniki do 3

## Przykladowy output
```
--- Treningi cardio ---
1. Bieganie | 45 min | 400 kcal | 2025-01-15
2. Rower | 60 min | 500 kcal | 2025-01-14

--- Treningi > 30 min (posortowane po dacie) ---
...

--- Top 3 najdluzsze treningi cardio ---
1. Rower | 60 min
2. Bieganie | 45 min
3. Plywanie | 40 min
```
