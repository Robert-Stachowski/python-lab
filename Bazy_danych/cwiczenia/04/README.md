# 04 - Sklep z produktami (Agregacje)

## Trudnosc: ⭐⭐ (Sredniozaawansowany)

## Cel
Przecwicz funkcje agregujace: COUNT, SUM, AVG, MIN, MAX z GROUP BY.

## Baza danych
- **SQLite** (plik `shop.db`)

## Model danych

### Category (Kategoria)
| Kolumna | Typ | Ograniczenia |
|---------|-----|-------------|
| id | Integer | Primary Key |
| name | String(100) | NOT NULL, UNIQUE |

### Product (Produkt)
| Kolumna | Typ | Ograniczenia |
|---------|-----|-------------|
| id | Integer | Primary Key |
| name | String(200) | NOT NULL |
| price | Float | NOT NULL |
| quantity | Integer | NOT NULL, default=0 |
| category_id | Integer | ForeignKey -> Category.id |

### Relacja
- Category -> Product: 1:N

## Zadania

### Zadanie 1: Seedowanie danych
- Dodaj 4 kategorie: Elektronika, Odziez, Ksiazki, Sport
- Dodaj po 3-5 produktow w kazdej kategorii z roznymi cenami i ilosciami

### Zadanie 2: Podstawowe agregacje
- Policz laczna liczbe produktow w sklepie (COUNT)
- Oblicz srednia cene wszystkich produktow (AVG)
- Znajdz najtanszy i najdrozszy produkt (MIN, MAX)
- Oblicz laczna wartosc magazynu: SUM(price * quantity)

### Zadanie 3: Agregacje z GROUP BY
- Policz ile produktow jest w kazdej kategorii
- Oblicz srednia cene produktow w kazdej kategorii
- Znajdz kategorie z laczna wartoscia magazynu > 1000 zl (HAVING)

### Zadanie 4: Zaawansowane zapytania
- Znajdz 5 najdrozszych produktow (ORDER BY + LIMIT)
- Znajdz produkty, ktorych jest mniej niz 5 sztuk (niski stan magazynowy)
- Wyswietl kategorie posortowane po liczbie produktow malejaco

## Podpowiedzi
- `from sqlalchemy import func`
- `func.count()`, `func.avg()`, `func.sum()`, `func.min()`, `func.max()`
- `session.query(func.count(Product.id)).scalar()`
- `group_by(Product.category_id)`
- `having(func.sum(...) > 1000)`

## Przykladowy output
```
--- Statystyki sklepu ---
Laczna liczba produktow: 16
Srednia cena: 245.50 zl
Najtanszy: Dlugopis (2.50 zl)
Najdrozszy: Laptop (4500.00 zl)
Wartosc magazynu: 52340.00 zl

--- Produkty na kategorie ---
Elektronika: 4 produkty (srednia: 1250.00 zl)
Odziez: 5 produktow (srednia: 120.00 zl)
Ksiazki: 4 produkty (srednia: 35.00 zl)
Sport: 3 produkty (srednia: 180.00 zl)

--- Kategorie z wartoscia > 1000 zl ---
Elektronika: 25000.00 zl
Sport: 3600.00 zl
```
