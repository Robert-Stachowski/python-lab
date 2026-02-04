"""
sqlalchemy_joins_orm_demo.py

Cel:
- Jeden kopiowalny plik .py: JOINy w SQLAlchemy ORM na prostych przykładach.
- Masz to wrzucić na Gita jako "ściągę na za 3 miesiące".

Co tu jest:
1) INNER JOIN (join)
2) LEFT OUTER JOIN (outerjoin)
3) JOIN + filter (warunek po drugiej tabeli)
4) JOIN po relacji (ORM relationship)
5) SQLAlchemy 2.0 style: select().join().where()
6) Prosty przykład "policz posty na usera" (GROUP BY)

Jak uruchomić:
pip install sqlalchemy
python sqlalchemy_joins_orm_demo.py

Uwaga:
- Demo na SQLite in-memory (żeby było samowystarczalne).
- W realnym projekcie podmieniasz engine na PostgreSQL.
"""

from __future__ import annotations

from datetime import datetime
from sqlalchemy import (
    create_engine,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Boolean,
    Text,
    select,
    func,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    Session,
)


# =============================================================================
# 1) MODELE (minimalne, ale "realne")
# =============================================================================

class Base(DeclarativeBase):
    """Bazowa klasa dla modeli SQLAlchemy."""
    pass


class User(Base):
    """
    User:
    - ma wiele Post (relacja 1:N)
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # relationship() = ORM-owa "mapa" relacji. Nie robi JOIN sam z siebie w kodzie,
    # ale pozwala pisać join(User.posts) albo post.user.
    posts: Mapped[list["Post"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",  # jak usuniesz usera, jego posty też (demo)
    )

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username!r})"


class Post(Base):
    """
    Post:
    - należy do User (user_id -> users.id)
    """
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)

    body: Mapped[str | None] = mapped_column(Text, nullable=True)

    # FK = Foreign Key = klucz obcy
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)

    # relacja "w drugą stronę": post.user
    user: Mapped[User | None] = relationship(back_populates="posts")

    def __repr__(self) -> str:
        return f"Post(id={self.id}, title={self.title!r}, user_id={self.user_id!r})"


# =============================================================================
# 2) SEED + PRINTY
# =============================================================================

def seed_data(session: Session) -> None:
    """
    Wrzucamy przykładowe dane.

    Ważne: jeden Post ma user_id=None, żeby pokazać różnicę między INNER JOIN a LEFT JOIN.
    """
    admin = User(username="admin", email="admin@gmail.com", is_active=True, deleted_at=None)
    ania = User(username="ania", email="ania@corp.com", is_active=False, deleted_at=None)
    bob = User(username="bob", email="bob@corp.com", is_active=True, deleted_at=datetime(2024, 1, 10))  # soft-delete

    # Posty admina
    admin.posts = [
        Post(title="Welcome", body="Hello world"),
        Post(title="SQLAlchemy tips", body="JOINs are everywhere"),
    ]

    # Ania ma 1 post
    ania.posts = [
        Post(title="Draft", body=None),
    ]

    # Post bez usera (osierocony) - celowo:
    orphan = Post(title="Orphan post", body="no user_id", user_id=None)

    session.add_all([admin, ania, bob, orphan])
    session.commit()


def print_title(title: str) -> None:
    print("\n" + "=" * 90)
    print(title)
    print("=" * 90)


def print_rows(label: str, rows: list[tuple]) -> None:
    print(f"\n{label}")
    for row in rows:
        print(" -", row)


# =============================================================================
# 3) JOINY: praktyczne wzory
# =============================================================================

def demo_query_style(session: Session) -> None:
    """
    Styl "klasyczny" (często spotkasz w kodzie):
    session.query(...).join(...).filter(...)

    To jest nadal normalne i działa, chociaż SQLAlchemy 2.0 promuje select().
    """
    print_title("A) INNER JOIN (join) — tylko rekordy z dopasowaniem po obu stronach")

    # INNER JOIN:
    # - pokaże tylko posty, które MAJĄ usera (user_id != NULL i pasuje do users.id)
    rows = (
        session.query(User.username, Post.title)
        .join(Post, User.id == Post.user_id)   # jawny warunek join
        .all()
    )
    print_rows("User.username + Post.title (INNER JOIN)", rows)

    print_title("B) LEFT OUTER JOIN (outerjoin) — wszyscy z lewej, nawet bez dopasowania")

    # LEFT OUTER JOIN:
    # - pokaże wszystkich userów
    # - jeśli user nie ma postów -> Post.title będzie None
    rows = (
        session.query(User.username, Post.title)
        .outerjoin(Post, User.id == Post.user_id)
        .order_by(User.username)
        .all()
    )
    print_rows("User.username + Post.title (LEFT JOIN)", rows)

    print_title("C) JOIN + filter po drugiej tabeli — najczęstszy realny przypadek")

    # "Daj mi posty użytkownika admin"
    rows = (
        session.query(Post.id, Post.title, User.username)
        .join(User, User.id == Post.user_id)
        .filter(User.username == "admin")
        .all()
    )
    print_rows("Posty admina (JOIN + filter(User.username=='admin'))", rows)

    print_title("D) JOIN po relacji (bez ręcznego warunku) — ORM robi to za Ciebie")

    # Tu korzystasz z relationship:
    # join(User.posts) = SQLAlchemy wie, że Post.user_id łączy się z User.id
    rows = (
        session.query(User.username, Post.title)
        .join(User.posts)  # join po relacji
        .all()
    )
    print_rows("JOIN po relacji: join(User.posts)", rows)

    print_title("E) Zagnieżdżanie: JOIN + kilka warunków (AND domyślnie)")

    # "Daj posty aktywnych userów, którzy nie są soft-deleted"
    rows = (
        session.query(Post.title, User.username)
        .join(Post.user)  # join po relacji w drugą stronę
        .filter(
            User.is_active == True,
            User.deleted_at.is_(None),
        )
        .all()
    )
    print_rows("Posty aktywnych i nieusuniętych userów", rows)


def demo_select_style(session: Session) -> None:
    """
    Styl SQLAlchemy 2.0:
    stmt = select(...).join(...).where(...)
    session.execute(stmt).all() / scalars()

    Ten styl jest coraz częściej polecany.
    """
    print_title("F) SQLAlchemy 2.0 style: select().join().where()")

    # select kolumn:
    stmt = (
        select(User.username, Post.title)
        .join(Post, User.id == Post.user_id)  # INNER JOIN
        .where(User.username == "admin")      # filtr
    )
    rows = session.execute(stmt).all()
    print_rows("select(User.username, Post.title) + join + where", rows)

    print_title("G) LEFT JOIN w 2.0: outerjoin()")

    stmt = (
        select(User.username, Post.title)
        .outerjoin(Post, User.id == Post.user_id)
        .order_by(User.username)
    )
    rows = session.execute(stmt).all()
    print_rows("select + outerjoin (LEFT JOIN)", rows)


def demo_group_by_counts(session: Session) -> None:
    """
    Bardzo częsty case w backendzie:
    - lista userów + liczba postów

    Tu wchodzi GROUP BY + COUNT.
    """
    print_title("H) Liczenie: User + liczba Postów (LEFT JOIN + GROUP BY + COUNT)")

    # LEFT JOIN, żeby user bez postów miał 0
    stmt = (
        select(
            User.username,
            func.count(Post.id).label("posts_count"),
        )
        .outerjoin(Post, User.id == Post.user_id)
        .group_by(User.id)
        .order_by(User.username)
    )

    rows = session.execute(stmt).all()
    print_rows("username + posts_count", rows)


# =============================================================================
# 4) MAIN
# =============================================================================

def main() -> None:
    # SQLite in-memory: szybkie, czyste demo
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=False)

    # tworzenie tabel
    Base.metadata.create_all(engine)

    # praca w sesji
    with Session(engine) as session:
        seed_data(session)

        # JOINy w stylu query()
        demo_query_style(session)

        # JOINy w stylu select() (2.0)
        demo_select_style(session)

        # Agregacja: count postów na usera
        demo_group_by_counts(session)


if __name__ == "__main__":
    main()
