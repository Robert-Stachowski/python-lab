# 03 - Biblioteka (Relacja jeden-do-wielu)

## Trudnosc: ⭐⭐ (Sredniozaawansowany)

## Cel
Przecwicz relacje jeden-do-wielu (1:N) z ForeignKey i relationship().

## Baza danych
- **SQLite** (plik `library.db`)

## Model danych

### Author (Autor)
| Kolumna | Typ | Ograniczenia |
|---------|-----|-------------|
| id | Integer | Primary Key |
| name | String(100) | NOT NULL |
| country | String(50) | opcjonalny |

### Book (Ksiazka)
| Kolumna | Typ | Ograniczenia |
|---------|-----|-------------|
| id | Integer | Primary Key |
| title | String(200) | NOT NULL |
| year | Integer | opcjonalny |
| author_id | Integer | ForeignKey -> Author.id, NOT NULL |

### Relacja
- Author -> Book: jeden autor moze miec wiele ksiazek
- Uzyj `relationship()` z `back_populates`
- Uzyj `cascade="all, delete-orphan"` na stronie autora

## Zadania

### Zadanie 1: Modele i seedowanie
- Zdefiniuj modele Author i Book z relacja 1:N
- Dodaj 3 autorow, kazdy z co najmniej 2 ksiazkami

### Zadanie 2: Zapytania relacyjne
- Wyswietl wszystkie ksiazki danego autora (przez relacje)
- Wyswietl autora danej ksiazki (przez relacje odwrotna)
- Uzyj `selectinload()` do eager loading

### Zadanie 3: Agregacje
- Policz ile ksiazek ma kazdy autor (GROUP BY + COUNT)
- Znajdz autora z najwieksza liczba ksiazek (HAVING)
- Wyswietl sredni rok wydania ksiazek kazdego autora

### Zadanie 4: Kaskadowe usuwanie
- Usun autora i sprawdz czy jego ksiazki tez zostaly usuniete

## Podpowiedzi
- `relationship("Book", back_populates="author", cascade="all, delete-orphan")`
- `from sqlalchemy.orm import selectinload`
- `session.query(Author).options(selectinload(Author.books))`
- `func.count()`, `func.avg()` z `from sqlalchemy import func`
- `group_by()`, `having()`

## Przykladowy output
```
--- Ksiazki Henryka Sienkiewicza ---
1. Quo Vadis (1896)
2. Krzyzacy (1900)
3. Potop (1886)

--- Autor ksiazki "Solaris" ---
Stanislaw Lem

--- Liczba ksiazek na autora ---
Henryk Sienkiewicz: 3 ksiazki
Stanislaw Lem: 2 ksiazki
Adam Mickiewicz: 2 ksiazki

--- Usuwanie autora ---
Usunieto: Adam Mickiewicz (wraz z 2 ksiazkami)
```
