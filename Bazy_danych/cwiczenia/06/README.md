# 06 - Paginacja i wyszukiwarka

## Trudnosc: ⭐⭐⭐ (Sredniozaawansowany+)

## Cel
Przecwicz paginacje wynikow (LIMIT/OFFSET) oraz wyszukiwanie tekstowe (LIKE/ILIKE).

## Baza danych
- **SQLite** (plik `movies.db`)

## Model danych

### Movie (Film)
| Kolumna | Typ | Ograniczenia |
|---------|-----|-------------|
| id | Integer | Primary Key |
| title | String(200) | NOT NULL |
| director | String(100) | NOT NULL |
| year | Integer | NOT NULL |
| genre | String(50) | NOT NULL |
| rating | Float | default=0.0 |

## Zadania

### Zadanie 1: Seedowanie
- Dodaj co najmniej 25 filmow roznych gatunkow i lat
- Uzyj roznych rezyserow i ocen

### Zadanie 2: Paginacja
- Zaimplementuj funkcje `get_page(session, page, per_page)` ktora zwraca filmy na danej stronie
- Wyswietl strone 1, 2 i 3 (po 5 filmow na strone)
- Wyswietl informacje: "Strona X z Y (lacznie Z filmow)"

### Zadanie 3: Wyszukiwanie tekstowe
- Wyszukaj filmy po fragmencie tytulu (LIKE/ilike)
- Wyszukaj filmy danego rezysera (case-insensitive)
- Wyszukaj filmy po gatunku i zakresie lat (np. "dramat" z lat 2000-2020)

### Zadanie 4: Laczenie paginacji z wyszukiwaniem
- Zaimplementuj `search_movies(session, query, page, per_page)` - wyszukiwanie z paginacja
- Wyszukaj filmy z slowem "the" w tytule, strona 1, po 3 na strone

### Zadanie 5: Sortowanie z paginacja
- Wyswietl filmy posortowane po ocenie (najlepsze pierwsze), strona 1
- Wyswietl filmy posortowane po roku (najnowsze), z paginacja

## Podpowiedzi
- Paginacja: `offset = (page - 1) * per_page`, potem `.offset(offset).limit(per_page)`
- Laczna liczba stron: `import math; total_pages = math.ceil(total / per_page)`
- LIKE: `Movie.title.like("%fragment%")` (case-sensitive)
- ILIKE: `Movie.title.ilike("%fragment%")` (case-insensitive)
- Zakres: `filter(Movie.year.between(2000, 2020))`

## Przykladowy output
```
--- Strona 1 z 5 (lacznie 25 filmow) ---
1. Skazani na Shawshank (1994) - Dramat - 9.3
2. Ojciec chrzestny (1972) - Dramat - 9.2
3. Mroczny Rycerz (2008) - Akcja - 9.0
4. Pulp Fiction (1994) - Kryminal - 8.9
5. Forrest Gump (1994) - Dramat - 8.8

--- Wyszukiwanie: "dark" ---
Znaleziono 2 wyniki:
1. Mroczny Rycerz (The Dark Knight)
2. Dark City

--- Wyszukiwanie z paginacja: "the", strona 1/2 ---
...
```
