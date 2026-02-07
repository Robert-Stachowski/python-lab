# Bazy danych - Ćwiczenia praktyczne

## SQLAlchemy ORM | SQLite + PostgreSQL

10 ćwiczeń praktycznych utrwalających wiedzę z baz danych, ułożonych od najprostszego.

## Spis ćwiczeń

| # | Nazwa | Trudność | Temat | Baza |
|---|-------|----------|-------|------|
| 01 | [Kontakty](cwiczenia/01/) | ⭐ | Podstawowy CRUD | SQLite |
| 02 | [Dziennik treningow](cwiczenia/02/) | ⭐ | Filtrowanie i sortowanie | SQLite |
| 03 | [Biblioteka](cwiczenia/03/) | ⭐⭐ | Relacja 1:N (Author-Book) | SQLite |
| 04 | [Sklep z produktami](cwiczenia/04/) | ⭐⭐ | Agregacje (COUNT, AVG, SUM) | SQLite |
| 05 | [System tagow](cwiczenia/05/) | ⭐⭐⭐ | Relacja N:M (tabela asocjacyjna) | SQLite |
| 06 | [Paginacja i wyszukiwarka](cwiczenia/06/) | ⭐⭐⭐ | LIMIT, OFFSET, LIKE | SQLite |
| 07 | [System uczniow i kursow](cwiczenia/07/) | ⭐⭐⭐ | Wiele relacji (1:N + N:M) | SQLite |
| 08 | [Analityka sprzedazy](cwiczenia/08/) | ⭐⭐⭐⭐ | Subquery, HAVING, raporty | PostgreSQL |
| 09 | [System rezerwacji](cwiczenia/09/) | ⭐⭐⭐⭐ | Transakcje, rollback, walidacja | PostgreSQL |
| 10 | [Blog CMS](cwiczenia/10/) | ⭐⭐⭐⭐⭐ | Kompletny system (5 modeli) | PostgreSQL |

## Umiejętności ćwiczone

- CRUD (Create, Read, Update, Delete)
- Filtrowanie i sortowanie (filter, order_by)
- Relacje 1:N (ForeignKey, relationship)
- Relacje N:M (Table, secondary)
- Agregacje (func.count, func.avg, func.sum, func.min, func.max)
- GROUP BY i HAVING
- Subquery (scalar_subquery)
- Paginacja (LIMIT, OFFSET)
- Wyszukiwanie tekstowe (LIKE, ILIKE)
- Transakcje i rollback
- Eager loading (selectinload)
- Cascade delete
- Obsługa błędów (SQLAlchemyError)

## Jak pracować z ćwiczeniami

1. Wejdź do folderu ćwiczenia (np. `cd cwiczenia/01`)
2. Przeczytaj `README.md` - opis zadania
3. Skopiuj `.env.example` do `.env`
4. Wypełnij szablony plików (`models.py`, `db.py`, `main.py`)
5. Uruchom: `python main.py`

## Wymagania

```bash
pip install sqlalchemy python-dotenv
# Dla ćwiczeń 08-10 dodatkowo:
pip install psycopg2-binary
```
