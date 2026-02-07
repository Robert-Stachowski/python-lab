from models import Base, Article, Tag
from db import engine, SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func


def create_tables():
    """Tworzy tabele w bazie danych."""
    Base.metadata.create_all(engine)


def seed_data(session):
    """Zadanie 1: Dodaj artykuly i tagi."""
    # TODO: Utworz artykuly, tagi i przypisz tagi do artykulow
    pass


def tags_of_article(session, title):
    """Zadanie 2a: Wyswietl tagi artykulu."""
    # TODO: Znajdz artykul i wyswietl jego tagi
    pass


def articles_with_tag(session, tag_name):
    """Zadanie 2b: Wyswietl artykuly z danym tagiem."""
    # TODO: Uzyj Article.tags.any()
    pass


def articles_with_both_tags(session, tag1, tag2):
    """Zadanie 2c: Artykuly z obydwoma tagami."""
    # TODO: Polacz dwa filtry any()
    pass


def add_tag_to_article(session, title, tag_name):
    """Zadanie 3a: Dodaj tag do artykulu."""
    # TODO: Uzyj article.tags.append(tag)
    pass


def remove_tag_from_article(session, title, tag_name):
    """Zadanie 3b: Usun tag z artykulu."""
    # TODO: Uzyj article.tags.remove(tag)
    pass


def replace_tags(session, title, new_tag_names):
    """Zadanie 3c: Zamien wszystkie tagi artykulu."""
    # TODO: Wyczysc tagi i dodaj nowe
    pass


def count_articles_per_tag(session):
    """Zadanie 4a: Policz artykuly na tag."""
    # TODO: Uzyj func.count() z group_by
    pass


def most_popular_tag(session):
    """Zadanie 4b: Najpopularniejszy tag."""
    # TODO: Uzyj order_by(desc) z limit(1)
    pass


def articles_without_tags(session):
    """Zadanie 4c: Artykuly bez tagow."""
    # TODO: Uzyj ~Article.tags.any()
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
