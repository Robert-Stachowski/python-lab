"""
sqlalchemy_aggregation_grouping_pagination.py

Cel:
- Agregacja + grupowanie + paginacja w SQLAlchemy ORM.

Co tu jest:
1) Agregacje: COUNT / SUM / AVG / MIN / MAX
2) GROUP BY + HAVING
3) Agregacje na JOIN (User + Post)
4) Paginacja OFFSET/LIMIT (klasyczna)
5) Paginacja keyset (lepsza wydajność w większych tabelach)
6) Sortowanie, bo bez ORDER BY paginacja jest "losowa"

Jak uruchomić:
pip install sqlalchemy
python sqlalchemy_aggregation_grouping_pagination.py
"""

from __future__ import annotations  # pozwala używać typów jako stringi (np. list["Post"])
from datetime import datetime  # tylko do przykładowych dat
from sqlalchemy import (
    create_engine,  # tworzy połączenie do bazy
    Integer,  # typ kolumny INT
    String,  # typ kolumny VARCHAR
    ForeignKey,  # klucz obcy
    DateTime,  # typ daty/czasu
    Boolean,  # typ bool
    select,  # SQLAlchemy 2.0 style: SELECT ...
    func,  # funkcje SQL: count/sum/avg/min/max
    desc,  # DESC w order_by
)
from sqlalchemy.orm import (
    DeclarativeBase,  # baza dla modeli ORM
    Mapped,  # typowanie pól ORM
    mapped_column,  # definiowanie kolumn w modelach
    relationship,  # relacje ORM
    Session,  # sesja (unit of work)
)


# =============================================================================
# 1) MODELE (proste, ale wystarczą do agregacji/grupowania/paginacji)
# =============================================================================

class Base(DeclarativeBase):
    """Bazowa klasa dla modeli ORM."""
    pass


class User(Base):
    """Użytkownik, który może mieć wiele postów."""
    __tablename__ = "users"  # nazwa tabeli w bazie

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # PK: primary key
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)  # unikalny login
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)  # czy aktywny
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)  # soft delete

    posts: Mapped[list["Post"]] = relationship(  # relacja 1:N
        back_populates="user",  # powiązanie z Post.user
        cascade="all, delete-orphan",  # demo: usuwanie usera usuwa posty
    )

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username!r})"


class Post(Base):
    """Post, który należy do usera i ma np. liczbę polubień (likes) do agregacji SUM/AVG."""
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # PK
    title: Mapped[str] = mapped_column(String(200), nullable=False)  # tytuł
    likes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)  # liczba polubień (pod SUM/AVG)

    user_id: Mapped[int | None] = mapped_column(  # FK, może być NULL (żeby pokazać LEFT JOIN)
        ForeignKey("users.id"),
        nullable=True,
    )

    user: Mapped[User | None] = relationship(  # relacja N:1
        back_populates="posts",
    )

    def __repr__(self) -> str:
        return f"Post(id={self.id}, title={self.title!r}, likes={self.likes}, user_id={self.user_id!r})"


# =============================================================================
# 2) SEED DANYCH (żeby demo było samowystarczalne)
# =============================================================================

def seed_data(session: Session) -> None:
    """Wrzuca kilka rekordów. Celowo: jeden user bez postów, jeden post bez usera."""
    admin = User(username="admin", is_active=True, deleted_at=None)  # aktywny
    ania = User(username="ania", is_active=False, deleted_at=None)  # nieaktywna
    bob = User(username="bob", is_active=True, deleted_at=datetime(2024, 1, 10))  # soft-deleted
    ola = User(username="ola", is_active=True, deleted_at=None)  # user bez postów (ważne dla LEFT JOIN)

    # posty admina
    admin.posts = [
        Post(title="Welcome", likes=10),
        Post(title="ORM tips", likes=25),
        Post(title="SQL vs ORM", likes=5),
    ]

    # posty ani
    ania.posts = [
        Post(title="Draft", likes=0),
        Post(title="Another draft", likes=2),
    ]

    # post osierocony (bez usera) -> pokaże różnicę INNER vs LEFT JOIN
    orphan = Post(title="Orphan post", likes=7, user_id=None)

    session.add_all([admin, ania, bob, ola, orphan])  # dodajemy wszystko do sesji
    session.commit()  # zapis do bazy


# =============================================================================
# 3) PRINTY (czytelny output)
# =============================================================================

def print_title(title: str) -> None:
    """Nagłówek sekcji w konsoli."""
    print("\n" + "=" * 100)
    print(title)
    print("=" * 100)


def print_rows(label: str, rows: list[tuple]) -> None:
    """Wypisuje wiersze wyników (krotki)."""
    print(f"\n{label}")
    for row in rows:
        print(" -", row)


# =============================================================================
# 4) AGREGACJA + GRUPOWANIE (GROUP BY / HAVING)
# =============================================================================

def demo_basic_aggregations(session: Session) -> None:
    """Podstawowe agregacje na tabeli posts."""
    print_title("A) Podstawowe agregacje na Posts: COUNT / SUM / AVG / MIN / MAX")

    stmt = select(
        func.count(Post.id).label("posts_count"),  # COUNT(id)
        func.sum(Post.likes).label("likes_sum"),  # SUM(likes)
        func.avg(Post.likes).label("likes_avg"),  # AVG(likes)
        func.min(Post.likes).label("likes_min"),  # MIN(likes)
        func.max(Post.likes).label("likes_max"),  # MAX(likes)
    )

    rows = session.execute(stmt).all()  # jedna krotka z wynikami agregacji
    print_rows("Agregacje globalne na tabeli posts", rows)


def demo_group_by_user_counts(session: Session) -> None:
    """GROUP BY: liczba postów i suma lajków na użytkownika."""
    print_title("B) GROUP BY: liczba postów i suma lajków per użytkownik (LEFT JOIN)")

    # LEFT JOIN, żeby user bez postów też był w wynikach z 0
    stmt = (
        select(
            User.username,
            func.count(Post.id).label("posts_count"),
            func.coalesce(func.sum(Post.likes), 0).label("likes_sum"),  # COALESCE -> NULL zamienia na 0
            func.coalesce(func.avg(Post.likes), 0).label("likes_avg"),
        )
        .outerjoin(Post, User.id == Post.user_id)  # LEFT JOIN users -> posts
        .group_by(User.id)  # grupowanie po userze
        .order_by(User.username)  # stabilna kolejność wyników
    )

    rows = session.execute(stmt).all()
    print_rows("username + posts_count + likes_sum + likes_avg", rows)


def demo_having(session: Session) -> None:
    """HAVING: filtr po agregacji (np. tylko userzy z >= 2 postami)."""
    print_title("C) HAVING: filtr po agregacji (np. userzy z >= 2 postami)")

    stmt = (
        select(
            User.username,
            func.count(Post.id).label("posts_count"),
        )
        .join(Post, User.id == Post.user_id)  # INNER JOIN -> tylko userzy mający posty
        .group_by(User.id)
        .having(func.count(Post.id) >= 2)  # HAVING (po agregacji)
        .order_by(desc(func.count(Post.id)))  # najpierw ci z większą liczbą postów
    )

    rows = session.execute(stmt).all()
    print_rows("Userzy z >= 2 postami (HAVING count>=2)", rows)


# =============================================================================
# 5) PAGINACJA (LIMIT/OFFSET + keyset)
# =============================================================================

def demo_offset_limit_pagination(session: Session) -> None:
    """
    Paginacja klasyczna: OFFSET/LIMIT.

    Plusy: prosta.
    Minusy: przy dużych tabelach OFFSET bywa wolny (baza musi 'przeskoczyć' wiele wierszy).
    """
    print_title("D) Paginacja OFFSET/LIMIT na Posts (ORDER BY + LIMIT + OFFSET)")

    page_size = 2  # ile rekordów na stronę
    page = 1  # strona 1 (0 = pierwsza, ale w API zwykle zaczyna się od 1)
    offset = (page - 1) * page_size  # wyliczenie przesunięcia

    stmt = (
        select(Post.id, Post.title, Post.likes, Post.user_id)
        .order_by(Post.id)  # UWAGA: bez ORDER BY paginacja jest nieprzewidywalna
        .limit(page_size)  # LIMIT
        .offset(offset)  # OFFSET
    )

    rows = session.execute(stmt).all()
    print_rows(f"Posts page={page}, page_size={page_size} (OFFSET/LIMIT)", rows)

    # Druga strona
    page = 2
    offset = (page - 1) * page_size

    stmt = (
        select(Post.id, Post.title, Post.likes, Post.user_id)
        .order_by(Post.id)
        .limit(page_size)
        .offset(offset)
    )

    rows = session.execute(stmt).all()
    print_rows(f"Posts page={page}, page_size={page_size} (OFFSET/LIMIT)", rows)


def demo_keyset_pagination(session: Session) -> None:
    """
    Paginacja keyset (aka "cursor pagination").

    Zasada:
    - nie używasz OFFSET
    - trzymasz "ostatnie id" z poprzedniej strony (last_id)
    - następna strona: WHERE id > last_id ORDER BY id LIMIT page_size

    To skaluje się dużo lepiej na dużych tabelach.
    """
    print_title("E) Paginacja keyset (cursor): WHERE id > last_id ORDER BY id LIMIT")

    page_size = 2  # rozmiar strony
    last_id = 0  # start: 0 (nic jeszcze nie widzieliśmy)

    # Strona 1
    stmt = (
        select(Post.id, Post.title)
        .where(Post.id > last_id)  # kluczowy warunek
        .order_by(Post.id)  # spójne sortowanie po tym samym kluczu
        .limit(page_size)
    )
    rows = session.execute(stmt).all()
    print_rows(f"Keyset page 1, last_id={last_id}", rows)

    # Ustalamy last_id jako ostatni id z wyników
    if rows:
        last_id = rows[-1][0]  # pierwsza kolumna w krotce to Post.id

    # Strona 2
    stmt = (
        select(Post.id, Post.title)
        .where(Post.id > last_id)
        .order_by(Post.id)
        .limit(page_size)
    )
    rows = session.execute(stmt).all()
    print_rows(f"Keyset page 2, last_id={last_id}", rows)


# =============================================================================
# 6) MAIN
# =============================================================================

def main() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=False)  # baza w RAM, do demo
    Base.metadata.create_all(engine)  # tworzymy tabele

    with Session(engine) as session:  # bezpieczny wzorzec sesji
        seed_data(session)  # dane testowe

        demo_basic_aggregations(session)  # agregacje globalne
        demo_group_by_user_counts(session)  # group by po userze
        demo_having(session)  # having (filtr po agregacji)

        demo_offset_limit_pagination(session)  # paginacja OFFSET/LIMIT
        demo_keyset_pagination(session)  # paginacja keyset


if __name__ == "__main__":
    main()
