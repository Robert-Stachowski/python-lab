from models import Base, Author, Book
from db import engine, SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from sqlalchemy import func


def create_tables():
    """Tworzy tabele w bazie danych."""
    Base.metadata.create_all(engine)


def seed_data(session):
    """Zadanie 1: Dodaj autorow z ksiazkami."""
    # TODO: Utworz autorow i przypisz im ksiazki
    pass


def books_by_author(session, author_name):
    """Zadanie 2a: Wyswietl ksiazki danego autora."""
    # TODO: Znajdz autora i wyswietl jego ksiazki przez relacje
    pass


def author_of_book(session, book_title):
    """Zadanie 2b: Wyswietl autora danej ksiazki."""
    # TODO: Znajdz ksiazke i wyswietl jej autora
    pass


def books_with_eager_loading(session):
    """Zadanie 2c: Uzyj selectinload do pobrania autorow z ksiazkami."""
    # TODO: Uzyj selectinload(Author.books)
    pass


def count_books_per_author(session):
    """Zadanie 3a: Policz ksiazki kazdego autora."""
    # TODO: Uzyj func.count() z group_by()
    pass


def author_with_most_books(session):
    """Zadanie 3b: Znajdz autora z najwieksza liczba ksiazek."""
    # TODO: Uzyj having() lub order_by z limit
    pass


def avg_year_per_author(session):
    """Zadanie 3c: Sredni rok wydania na autora."""
    # TODO: Uzyj func.avg()
    pass


def delete_author_cascade(session, author_name):
    """Zadanie 4: Usun autora kaskadowo."""
    # TODO: Usun autora i sprawdz czy ksiazki tez znikly
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
