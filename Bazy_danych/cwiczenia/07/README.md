# 07 - System uczniow i kursow (Wiele relacji)

## Trudnosc: ⭐⭐⭐ (Sredniozaawansowany+)

## Cel
Przecwicz laczenie wielu typow relacji (1:N i N:M) w jednym projekcie.

## Baza danych
- **SQLite** (plik `school.db`)

## Model danych

### Student (Uczen)
| Kolumna | Typ | Ograniczenia |
|---------|-----|-------------|
| id | Integer | Primary Key |
| name | String(100) | NOT NULL |
| email | String(100) | NOT NULL, UNIQUE |

### Course (Kurs)
| Kolumna | Typ | Ograniczenia |
|---------|-----|-------------|
| id | Integer | Primary Key |
| name | String(100) | NOT NULL |
| instructor | String(100) | NOT NULL |

### Grade (Ocena) - tabela posrednia z dodatkowymi danymi
| Kolumna | Typ | Ograniczenia |
|---------|-----|-------------|
| id | Integer | Primary Key |
| value | Float | NOT NULL (1.0 - 6.0) |
| date | Date | NOT NULL |
| student_id | Integer | FK -> Student.id |
| course_id | Integer | FK -> Course.id |

### Relacje
- Student -> Grade: 1:N (uczen ma wiele ocen)
- Course -> Grade: 1:N (kurs ma wiele ocen)
- Student <-> Course: N:M (przez tabele Grade - uczen moze byc na wielu kursach)

## Zadania

### Zadanie 1: Modele i seedowanie
- Zdefiniuj 3 modele z relacjami
- Dodaj 5 uczniow, 3 kursy
- Dodaj po kilka ocen (kazdy uczen ma oceny z co najmniej 2 kursow)

### Zadanie 2: Zapytania relacyjne
- Wyswietl wszystkie oceny danego ucznia (z nazwami kursow)
- Wyswietl wszystkich uczniow zapisanych na dany kurs
- Wyswietl oceny z danego kursu posortowane od najwyzszej

### Zadanie 3: Agregacje
- Oblicz srednia ocen kazdego ucznia
- Oblicz srednia ocen na kazdym kursie
- Znajdz ucznia z najwyzsza srednia
- Znajdz kurs z najnizsza srednia

### Zadanie 4: Zaawansowane zapytania
- Znajdz uczniow ktorzy maja co najmniej jedna ocene ponizej 3.0
- Wyswietl ranking uczniow (posortowanych po sredniej malejaco)
- Policz ile ocen wystawiono w kazdym miesiacu

## Podpowiedzi
- Grade to NIE jest zwykla tabela asocjacyjna - ma dodatkowe kolumny (value, date)
- Dlatego Grade jest pelnym modelem z relacjami 1:N do Student i Course
- `func.avg(Grade.value)` do sredniej
- `func.extract('month', Grade.date)` do wyciagania miesiaca (SQLite: uzyj strftime)
- Dla SQLite zamiast extract uzyj: `func.strftime('%m', Grade.date)`

## Przykladowy output
```
--- Oceny ucznia: Jan Kowalski ---
Matematyka: 4.5 (2025-01-10)
Matematyka: 5.0 (2025-01-20)
Fizyka: 3.5 (2025-01-15)

--- Uczniowie na kursie: Matematyka ---
1. Jan Kowalski (srednia: 4.75)
2. Anna Nowak (srednia: 4.0)
3. Piotr Wisniewski (srednia: 3.5)

--- Ranking uczniow ---
1. Jan Kowalski - srednia: 4.33
2. Anna Nowak - srednia: 4.17
3. Piotr Wisniewski - srednia: 3.83
...
```
