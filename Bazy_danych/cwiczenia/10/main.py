from models import Base, User, Category, Post, Tag, Comment
from db import engine, SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from sqlalchemy import func


def create_tables():
    """Tworzy tabele w bazie danych."""
    Base.metadata.create_all(engine)


def seed_data(session):
    """Zadanie 1: Dodaj userow, kategorie, tagi, posty i komentarze."""
    # TODO: Kompletne seedowanie
    pass


def create_post(session, author_id, category_id, title, content, tag_names):
    """Zadanie 2a: Utworz nowy post z tagami."""
    # TODO: Utworz post i przypisz tagi
    pass


def edit_post(session, post_id, new_content):
    """Zadanie 2b: Edytuj tresc posta."""
    # TODO: Zaktualizuj content (updated_at powinno sie zmienic)
    pass


def publish_post(session, post_id):
    """Zadanie 2c: Opublikuj draft."""
    # TODO: Zmien is_published na True
    pass


def delete_post(session, post_id):
    """Zadanie 2d: Usun post kaskadowo."""
    # TODO: Usun post (komentarze powinny zniknac automatycznie)
    pass


def posts_by_author(session, username):
    """Zadanie 3a: Posty autora."""
    # TODO: Join z User
    pass


def comments_on_post(session, post_id):
    """Zadanie 3b: Komentarze pod postem."""
    # TODO: Join z User (autor komentarza)
    pass


def posts_in_category(session, category_name):
    """Zadanie 3c: Posty w kategorii."""
    pass


def posts_with_tag(session, tag_name):
    """Zadanie 3d: Posty z tagiem."""
    # TODO: Uzyj Article.tags.any()
    pass


def published_posts_with_tag(session, tag_name):
    """Zadanie 3e: Opublikowane posty z tagiem."""
    # TODO: Polacz filtr published + tag
    pass


def posts_per_author(session):
    """Zadanie 4a: Liczba postow na autora."""
    pass


def comments_per_post(session):
    """Zadanie 4b: Liczba komentarzy na post."""
    pass


def avg_comments_per_post(session):
    """Zadanie 4c: Srednia komentarzy na post."""
    # TODO: Uzyj subquery
    pass


def most_popular_tag(session):
    """Zadanie 4d: Najpopularniejszy tag."""
    pass


def top_category(session):
    """Zadanie 4e: Kategoria z najwieksza liczba opublikowanych postow."""
    pass


def most_active_commenter(session):
    """Zadanie 4f: Najaktywniejszy komentujacy."""
    pass


def author_ranking(session):
    """Zadanie 5a: Ranking autorow."""
    pass


def posts_without_comments(session):
    """Zadanie 5b: Posty bez komentarzy."""
    # TODO: Uzyj ~Post.comments.any()
    pass


def posts_with_many_comments(session, min_count=3):
    """Zadanie 5c: Posty z > min_count komentarzy."""
    # TODO: Uzyj HAVING
    pass


def latest_comments(session, limit=5):
    """Zadanie 5d: Ostatnie komentarze."""
    pass


def draft_vs_published_per_author(session):
    """Zadanie 5e: Draft vs opublikowane na autora."""
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
