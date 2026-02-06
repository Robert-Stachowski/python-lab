# SQLAlchemy ORM

Nauka ORM: sesje, modele, filtrowanie, JOINy, relacje, agregacje.

## Zawartosc

| Plik | Opis |
|------|------|
| `connect_db.py` | Połączenie z bazą przez .env (engine + SessionLocal) |
| `many_to_many_db.py` | Relacja many-to-many (User <-> Group) z demo CRUD |
| `tutorial_link.py` | Link do zewnętrznego tutoriala na GitHubie |

### krok_po_kroku/

Progresywna nauka od sesji do gotowej aplikacji:

| Plik | Opis |
|------|------|
| `step_1_tworzenie_sesji.py` | Tworzenie engine i Session (SQLite/PostgreSQL) |
| `step_2_tworzenie_tabeli.py` | Definicja modelu User z DeclarativeBase |
| `step_3_tworzenie_main.py` | Łączenie sesji + modelu, CRUD z duplikat-check |

### ściągi/

Wzorce do szybkiego przypomnienia:

| Plik | Opis |
|------|------|
| `filtering_patterns.py` | Filtrowanie: ==, !=, >, LIKE, IN, BETWEEN, AND/OR/NOT |
| `join_patterns.py` | JOINy: INNER, LEFT, z filtrami, GROUP BY + COUNT |
| `aggregation_pagination.py` | Agregacje (COUNT/SUM/AVG), GROUP BY, OFFSET/LIMIT, keyset pagination |

## Wymagania

- Plik `.env` z `DATABASE_URL` (przykład: `sqlite:///test.db`)
- `pip install sqlalchemy python-dotenv`
