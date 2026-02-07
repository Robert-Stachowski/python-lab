from models import Base, Movie
from db import engine, SessionLocal
from sqlalchemy.exc import SQLAlchemyError
import math


def create_tables():
    """Tworzy tabele w bazie danych."""
    Base.metadata.create_all(engine)


def seed_movies(session):
    """Zadanie 1: Dodaj co najmniej 25 filmow."""
    # TODO: Utworz liste filmow i dodaj do bazy
    pass


def get_page(session, page, per_page=5):
    """Zadanie 2: Pobierz filmy z danej strony."""
    # TODO: Oblicz offset, uzyj limit i offset
    # TODO: Oblicz laczna liczbe stron
    pass


def search_by_title(session, fragment):
    """Zadanie 3a: Wyszukaj po fragmencie tytulu."""
    # TODO: Uzyj ilike("%fragment%")
    pass


def search_by_director(session, director_name):
    """Zadanie 3b: Wyszukaj po rezyserze."""
    # TODO: Uzyj ilike
    pass


def search_by_genre_and_years(session, genre, year_from, year_to):
    """Zadanie 3c: Wyszukaj po gatunku i zakresie lat."""
    # TODO: Uzyj filter z between()
    pass


def search_movies(session, query, page=1, per_page=3):
    """Zadanie 4: Wyszukiwanie z paginacja."""
    # TODO: Polacz ilike z offset/limit
    pass


def sorted_page(session, sort_by="rating", page=1, per_page=5):
    """Zadanie 5: Sortowanie z paginacja."""
    # TODO: Polacz order_by z offset/limit
    pass


if __name__ == "__main__":
    create_tables()

    with SessionLocal() as session:
        try:
            # TODO: Wywolaj funkcje w odpowiedniej kolejnosci
            pass
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Blad bazy danych: {e}")
