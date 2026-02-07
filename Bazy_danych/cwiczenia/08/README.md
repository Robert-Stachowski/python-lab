# 08 - Analityka sprzedazy (Subquery i zaawansowane agregacje)

## Trudnosc: ⭐⭐⭐⭐ (Zaawansowany)

## Cel
Przecwicz subquery, having, zlaczone agregacje i zaawansowane zapytania analityczne.

## Baza danych
- **PostgreSQL** (wymaga serwera PostgreSQL)

## Model danych

### Customer (Klient)
| Kolumna | Typ | Ograniczenia |
|---------|-----|-------------|
| id | Integer | Primary Key |
| name | String(100) | NOT NULL |
| email | String(100) | NOT NULL, UNIQUE |
| city | String(100) | NOT NULL |

### Product (Produkt)
| Kolumna | Typ | Ograniczenia |
|---------|-----|-------------|
| id | Integer | Primary Key |
| name | String(200) | NOT NULL |
| price | Float | NOT NULL |
| category | String(50) | NOT NULL |

### Order (Zamowienie)
| Kolumna | Typ | Ograniczenia |
|---------|-----|-------------|
| id | Integer | Primary Key |
| customer_id | Integer | FK -> Customer.id |
| product_id | Integer | FK -> Product.id |
| quantity | Integer | NOT NULL |
| order_date | DateTime | default=utcnow |

### Relacje
- Customer -> Order: 1:N
- Product -> Order: 1:N

## Zadania

### Zadanie 1: Seedowanie
- Dodaj 5 klientow z roznych miast
- Dodaj 10 produktow w 3 kategoriach
- Dodaj 20+ zamowien z roznymi datami

### Zadanie 2: Podstawowe agregacje
- Laczna wartosc wszystkich zamowien (SUM: price * quantity)
- Srednia wartosc zamowienia
- Liczba zamowien na klienta

### Zadanie 3: Subquery
- Znajdz klientow ktorzy wydali wiecej niz srednia (subquery)
- Znajdz produkty ktore nigdy nie byly zamowione (NOT IN subquery)
- Znajdz klienta z najwyzsza laczna kwota zamowien (subquery + order_by)

### Zadanie 4: HAVING i zaawansowane grupowanie
- Znajdz kategorie produktow z laczna sprzedaza > 500 zl (HAVING)
- Znajdz miasta z wiecej niz 3 zamowieniami
- Sprzedaz miesieczna (grupowanie po miesiacu)

### Zadanie 5: Raporty
- Top 3 najczesciej kupowane produkty
- Top 3 klienci (po lacznej kwocie)
- Raport: kategoria -> liczba zamowien -> laczna wartosc -> srednia wartosc

## Podpowiedzi
- Subquery: `subquery = session.query(func.avg(...)).scalar_subquery()`
- NOT IN: `~Product.id.in_(subquery)`
- HAVING: `.group_by(...).having(func.sum(...) > 500)`
- Wartosc zamowienia: `Product.price * Order.quantity`
- Join: `session.query(Customer, func.sum(...)).join(Order).join(Product)`
- Miesieczne grupowanie: `func.extract('month', Order.order_date)`

## Przykladowy output
```
--- Statystyki sprzedazy ---
Laczna wartosc: 15420.00 zl
Srednia zamowienie: 514.00 zl
Liczba zamowien: 30

--- Klienci powyzej sredniej ---
1. Jan Kowalski: 2500.00 zl
2. Anna Nowak: 1800.00 zl

--- Sprzedaz miesiczna ---
Styczen 2025: 3200.00 zl (8 zamowien)
Luty 2025: 4100.00 zl (10 zamowien)

--- Top 3 produkty ---
1. Laptop (15 zamowien)
2. Mysz bezprzewodowa (12 zamowien)
3. Klawiatura (9 zamowien)
```
