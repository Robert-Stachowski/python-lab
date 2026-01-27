"""
sqlalchemy_filtering_patterns_demo.py

Cel:
- Wzory filtrowania w SQLAlchemy ORM:
  filter(), filter_by(), operatory porównań, AND/OR/NOT, zagnieżdżanie, negacja,
  LIKE / ILIKE, IN, BETWEEN, NULL (IS NULL / IS NOT NULL).

Jak używać:
1) Zainstaluj SQLAlchemy:
   pip install sqlalchemy

2) Uruchom:
   python sqlalchemy_filtering_patterns_demo.py

Uwaga:
- To jest DEMO na SQLite (in-memory). W realnym projekcie podmieniam engine na Postgresa.
"""

from __future__ import annotations  # Ułatwia typowanie (opcjonalne, bezpieczne)
from dataclasses import dataclass  # Tylko do czytelności (nie wymagane)
from datetime import datetime  # Do przykładowych dat

from sqlalchemy import (
    Boolean,
    DateTime,
    Integer,
    String,
    Text,
    create_engine,
    select,
    and_,
    or_,
    not_,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


# =========================
# 1) MODEL + BAZA (DEMO)
# =========================

class Base(DeclarativeBase):
    """Bazowa klasa dla modeli SQLAlchemy (ORM)."""
    pass


class User(Base):
    """
    Minimalny model użytkownika pod filtrowanie.
    Celowo daję pola, które są typowe w backendzie.
    """
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)

    first_name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    city: Mapped[str | None] = mapped_column(String(50), nullable=True)

    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username!r}, email={self.email!r})"


def seed_data(session: Session) -> None:
    """Wrzuca przykładowe dane do bazy."""
    users = [
        User(
            username="admin",
            email="admin@gmail.com",
            first_name="Jan",
            city="Poznań",
            age=35,
            is_active=True,
            bio="Admin account",
            deleted_at=None,
        ),
        User(
            username="janek",
            email="jan.kowalski@example.com",
            first_name="Jan",
            city="Warszawa",
            age=17,
            is_active=True,
            bio=None,  # celowo NULL
            deleted_at=None,
        ),
        User(
            username="ania",
            email="ania.nowak@gmail.com",
            first_name="Anna",
            city="Poznań",
            age=28,
            is_active=False,
            bio="Lubi SQL",
            deleted_at=None,
        ),
        User(
            username="bob",
            email="bob@corp.com",
            first_name=None,  # celowo NULL
            city="Gdańsk",
            age=None,  # celowo NULL
            is_active=True,
            bio="Work account",
            deleted_at=datetime(2024, 1, 10),  # soft delete
        ),
        User(
            username="moderator",
            email="moderator@corp.com",
            first_name="Piotr",
            city="Warszawa",
            age=22,
            is_active=True,
            bio="Mod",
            deleted_at=None,
        ),
    ]
    session.add_all(users)
    session.commit()


# =========================
# 2) NARZĘDZIA DO WYDRUKU
# =========================

def print_title(title: str) -> None:
    """Ładny nagłówek w konsoli."""
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def print_results(label: str, rows: list[User]) -> None:
    """Wypisuje wynik zapytania."""
    print(f"\n{label}")
    for u in rows:
        print(f" - {u} | first_name={u.first_name!r} city={u.city!r} age={u.age!r} "
              f"is_active={u.is_active!r} bio={u.bio!r} deleted_at={u.deleted_at!r}")


# =========================
# 3) WZORY FILTROWANIA
# =========================

def patterns_query_api(session: Session) -> None:
    """
    Wzory filtrowania w stylu:
    session.query(User).filter(...)
    (Klasyczny styl 1.x, nadal spotykany w projektach)

    Jeśli używasz 2.0 style (select(User)), patrz funkcję patterns_select_api().
    """
    print_title("A) query() + filter_by() (tylko proste równości)")

    # filter_by() -> tylko równości (kolumna = wartość), bez OR/LIKE/>,< itd.
    rows = session.query(User).filter_by(first_name="Jan").all()
    print_results("filter_by(first_name='Jan')", rows)

    rows = session.query(User).filter_by(city="Poznań", is_active=True).all()
    print_results("filter_by(city='Poznań', is_active=True)  # AND domyślnie", rows)

    print_title("B) query() + filter() (pełna kontrola: operatory, logika, zagnieżdżenia)")

    # Operatory porównań: ==, !=, >, <, >=, <=
    rows = session.query(User).filter(User.age > 18).all()
    print_results("filter(User.age > 18)", rows)

    rows = session.query(User).filter(User.username != "admin").all()
    print_results("filter(User.username != 'admin')", rows)

    # NULL: NIE używaj `== None` w ciemno w innych bibliotekach, ale w SQLAlchemy to działa.
    # Czytelniej: .is_(None) i .is_not(None)
    rows = session.query(User).filter(User.bio.is_(None)).all()
    print_results("filter(User.bio.is_(None))  # IS NULL", rows)

    rows = session.query(User).filter(User.deleted_at.is_not(None)).all()
    print_results("filter(User.deleted_at.is_not(None))  # IS NOT NULL", rows)

    print_title("C) AND / OR / NOT, negacja, zagnieżdżanie")

    # AND: domyślnie, gdy podasz kilka warunków w filter()
    rows = session.query(User).filter(
        User.is_active == True,
        User.deleted_at.is_(None),
    ).all()
    print_results("AND: filter(User.is_active == True, User.deleted_at IS NULL)", rows)

    # OR: używaj or_()
    rows = session.query(User).filter(
        or_(
            User.city == "Poznań",
            User.city == "Warszawa",
        )
    ).all()
    print_results("OR: filter(or_(city='Poznań', city='Warszawa'))", rows)

    # NOT: używaj not_() lub operatora ~ (tylko na wyrażeniach SQLAlchemy)
    rows = session.query(User).filter(not_(User.is_active)).all()
    print_results("NOT: filter(not_(User.is_active))", rows)

    rows = session.query(User).filter(~User.is_active).all()
    print_results("NOT (skrót): filter(~User.is_active)", rows)

    # Zagnieżdżanie:
    # age > 18 AND (city='Poznań' OR city='Warszawa')
    rows = session.query(User).filter(
        User.age.is_not(None),
        User.age > 18,
        or_(
            User.city == "Poznań",
            User.city == "Warszawa",
        )
    ).all()
    print_results("Zagnieżdżanie: age>18 AND (city=Poznań OR city=Warszawa)", rows)

    print_title("D) LIKE / ILIKE, IN, BETWEEN")

    # LIKE: % = dowolny ciąg znaków
    rows = session.query(User).filter(User.email.like("%gmail%")).all()
    print_results("LIKE: filter(User.email.like('%gmail%'))", rows)

    # ILIKE: case-insensitive (na PostgreSQL działa natywnie; na SQLite zależy od collation)
    rows = session.query(User).filter(User.email.ilike("%GMAIL%")).all()
    print_results("ILIKE: filter(User.email.ilike('%GMAIL%'))", rows)

    # IN
    rows = session.query(User).filter(User.username.in_(["admin", "moderator"])).all()
    print_results("IN: filter(User.username.in_(['admin','moderator']))", rows)

    # BETWEEN (włącznie z końcami)
    rows = session.query(User).filter(User.age.between(18, 30)).all()
    print_results("BETWEEN: filter(User.age.between(18, 30))", rows)

    print_title("E) Pułapka #1: NIE używaj pythonowego and/or w warunkach SQLAlchemy")

    # ŹLE (wykona się w Pythonie, nie w SQL): (User.age > 18) and (User.is_active == True)
    # Poprawnie: and_() / or_() albo wiele argumentów do filter()
    rows = session.query(User).filter(
        and_(
            User.age.is_not(None),
            User.age > 18,
            User.is_active == True,
        )
    ).all()
    print_results("POPRAWNIE: filter(and_(age>18, is_active=True))", rows)

    rows = session.query(User).filter(
        or_(
            and_(User.city == "Poznań", User.is_active == True),
            and_(User.city == "Warszawa", User.is_active == True),
        )
    ).all()
    print_results("OR + AND (zagnieżdżone): aktywni z Poznania lub Warszawy", rows)


def patterns_select_api(session: Session) -> None:
    """
    Wzory filtrowania w stylu SQLAlchemy 2.0:
    stmt = select(User).where(...)
    session.execute(stmt).scalars().all()

    To jest kierunek, w którym idzie SQLAlchemy.
    """
    print_title("F) select() + where() (SQLAlchemy 2.0 style)")

    # where() działa podobnie jak filter(): możesz dawać wiele warunków (AND domyślnie)
    stmt = select(User).where(
        User.is_active == True,
        User.deleted_at.is_(None),
    )
    rows = session.execute(stmt).scalars().all()
    print_results("select(User).where(is_active=True, deleted_at IS NULL)", rows)

    # OR
    stmt = select(User).where(
        or_(
            User.first_name == "Jan",
            User.first_name == "Anna",
        )
    )
    rows = session.execute(stmt).scalars().all()
    print_results("select(User).where(or_(first_name='Jan', first_name='Anna'))", rows)

    # NOT
    stmt = select(User).where(~User.is_active)
    rows = session.execute(stmt).scalars().all()
    print_results("select(User).where(~User.is_active)", rows)


def main() -> None:
    # In-memory SQLite (do testów i demo)
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=False)

    # Tworzymy tabele
    Base.metadata.create_all(engine)

    # Pracujemy w sesji (najbezpieczniej: with Session(...))
    with Session(engine) as session:
        seed_data(session)

        # Wzory query()+filter()/filter_by()
        patterns_query_api(session)

        # Wzory select()+where()
        patterns_select_api(session)


if __name__ == "__main__":
    main()
