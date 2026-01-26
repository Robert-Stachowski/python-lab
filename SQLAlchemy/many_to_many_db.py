"""
many_to_many_example.py

Cel pliku:
- Pokazać relację wiele-do-wiele (Many-to-Many) w SQLAlchemy (ORM) na prostym przykładzie: User <-> Group.

1) Tabela pośrednia (association table) jako obiekt Table (bez klasy ORM).
2) Dwa modele ORM: User i Group.
3) Relationship z użyciem secondary + back_populates.
4) Mini-demo: tworzenie danych + przypisywanie użytkowników do grup.
5) Jak odczytywać relacje w obie strony.

Wymagania (lokalnie):
- SQLAlchemy (2.x działa najlepiej)
- Ten przykład używa SQLite (plik many_to_many_demo.db) żebyś nie musiał odpalać Postgresa.

Uruchomienie:
python many_to_many_example.py

UWAGA:
- To jest klasyczny many-to-many bez dodatkowych pól w tabeli pośredniej.
- Jeśli kiedyś chcesz mieć np. date_joined / role / status w powiązaniu User-Group,
  wtedy robisz „association object” (czyli osobną klasę ORM) – to jest inny wariant.
"""

from __future__ import annotations

from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
    create_engine,
    select,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    relationship,
    sessionmaker,
)


# ======================================================================
# 1) Baza dla modeli ORM
# ======================================================================

class Base(DeclarativeBase):
    """Bazowa klasa dla modeli ORM."""
    pass


# ======================================================================
# 2) Tabela pośrednia (association table) - bez klasy ORM
# ======================================================================

# Dlaczego Table, a nie class?
# - bo tabela pośrednia przechowuje tylko pary ID (user_id, group_id)
# - nie ma własnej logiki domenowej i nie jest używana "bezpośrednio"
# - ORM będzie robił INSERT/DELETE w tej tabeli automatycznie, gdy zmienisz relacje

user_groups = Table(
    "user_groups",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("group_id", Integer, ForeignKey("groups.id"), primary_key=True),
)

# primary_key=True na obu kolumnach:
# - to robi z pary (user_id, group_id) unikalny klucz
# - zapobiega duplikatom typu: (Kasia, Admin) dodane 2 razy


# ======================================================================
# 3) Modele ORM
# ======================================================================

class Group(Base):
    """
    Model grupy (np. Admin, Moderator).

    users:
    - lista obiektów User należących do tej grupy
    - secondary=user_groups oznacza: powiązanie idzie przez tabelę pośrednią
    - back_populates="groups" spina relację w obie strony
    """
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    users = relationship(
        "User",
        secondary=user_groups,
        back_populates="groups",
    )

    def __repr__(self) -> str:
        return f"Group(id={self.id}, name={self.name!r})"


class User(Base):
    """
    Model użytkownika (np. Kasia, Tomek).

    groups:
    - lista obiektów Group, do których należy użytkownik
    - secondary=user_groups oznacza: powiązanie idzie przez tabelę pośrednią
    - back_populates="users" spina relację w obie strony
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    groups = relationship(
        "Group",
        secondary=user_groups,
        back_populates="users",
    )

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name!r})"


# ======================================================================
# 4) Konfiguracja bazy + sesji
# ======================================================================

def create_session(db_url: str = "sqlite:///many_to_many_demo.db"):
    """
    Tworzy engine, odpala migrację "na szybko" (create_all) i zwraca sesję.

    W realnym projekcie:
    - zamiast create_all używasz migracji (Alembic).
    """
    engine = create_engine(db_url, echo=False)  # echo=True -> zobaczysz SQL w konsoli
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    return Session()


# ======================================================================
# 5) Funkcje pomocnicze do demo
# ======================================================================

def get_or_create_group(session, name: str) -> Group:
    """Zwraca grupę po nazwie, a jeśli nie istnieje - tworzy ją."""
    group = session.execute(select(Group).where(Group.name == name)).scalar_one_or_none()
    if group is None:
        group = Group(name=name)
        session.add(group)
        session.commit()
    return group


def create_user(session, name: str) -> User:
    """Tworzy użytkownika."""
    user = User(name=name)
    session.add(user)
    session.commit()
    return user


def print_users_with_groups(session) -> None:
    """
    Wypisuje użytkowników i ich grupy.
    Tu najlepiej widać, że user.groups zachowuje się jak lista.
    """
    users = session.execute(select(User)).scalars().all()

    print("\n=== USERS -> GROUPS ===")
    for user in users:
        group_names = [g.name for g in user.groups]
        print(f"- {user.name}: {group_names}")


def print_groups_with_users(session) -> None:
    """
    Wypisuje grupy i ich użytkowników.
    To pokazuje, że relacja działa w obie strony dzięki back_populates.
    """
    groups = session.execute(select(Group)).scalars().all()

    print("\n=== GROUPS -> USERS ===")
    for group in groups:
        user_names = [u.name for u in group.users]
        print(f"- {group.name}: {user_names}")


def print_raw_association_table(session) -> None:
    """
    Podgląd tego, co faktycznie siedzi w tabeli pośredniej.
    Normalnie nie musisz tego robić — to tylko dydaktycznie.
    """
    rows = session.execute(select(user_groups.c.user_id, user_groups.c.group_id)).all()

    print("\n=== RAW user_groups TABLE (user_id, group_id) ===")
    for row in rows:
        print(f"- user_id={row.user_id}, group_id={row.group_id}")


# ======================================================================
# 6) Mini-demo
# ======================================================================

def main() -> None:
    session = create_session()

    # --- Tworzymy grupy (albo pobieramy istniejące) ---
    admin = get_or_create_group(session, "Admin")
    moderator = get_or_create_group(session, "Moderator")
    user_group = get_or_create_group(session, "User")

    # --- Tworzymy użytkowników ---
    kasia = create_user(session, "Kasia")
    tomek = create_user(session, "Tomek")

    # --- Dodawanie relacji (jak praca na liście) ---
    # user.groups.append(group) -> ORM zrobi INSERT do user_groups po commit()
    kasia.groups.append(admin)
    kasia.groups.append(user_group)

    tomek.groups.append(moderator)
    tomek.groups.append(user_group)

    session.commit()

    # --- Odczyt relacji w obie strony ---
    print_users_with_groups(session)
    print_groups_with_users(session)

    # --- Dydaktycznie: zobacz, że tabela pośrednia ma same ID ---
    print_raw_association_table(session)

    # --- Usuwanie relacji ---
    # To nie usuwa usera ani grupy.
    # To usuwa tylko wiersz z tabeli pośredniej (user_id, group_id).
    kasia.groups.remove(user_group)
    session.commit()

    print("\n=== AFTER kasia.groups.remove('User') ===")
    print_users_with_groups(session)
    print_groups_with_users(session)
    print_raw_association_table(session)

    session.close()


if __name__ == "__main__":
    main()
