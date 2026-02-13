from models import Base, Article, Tag, article_tag
from db import engine, SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, desc
from datetime import  datetime, timedelta



def create_tables():
    """Tworzy tabele w bazie danych."""
    Base.metadata.create_all(engine)


def clear_tables(session):
    create_tables()
    session.execute(article_tag.delete())
    session.query(Tag).delete()
    session.query(Article).delete()


def seed_data(session):
    """Zadanie 1: Dodaj artykuły i tagi."""
    # TODO: Utwórz artykuły, tagi i przypisz tagi do artykułów
    
    
    python = Tag(name="python")
    sqlalchemy = Tag(name="sqlalchemy")
    orm = Tag(name="orm")
    backend = Tag(name="backend")
    testing = Tag(name="testing")
    django = Tag(name="django")
    api = Tag(name="api")
    performance = Tag(name="performance")
    basics = Tag(name="basics")

    session.add_all([
        python, sqlalchemy, orm, backend,
        testing, django, api, performance, basics
    ])

    now = datetime.utcnow()
    
    articles = [
        Article(
            title="Introduction to Python",
            content="Basics of Python programming for beginners.",
            created_at=now - timedelta(days=2),
            tags=[python, basics]
        ),
        Article(
            title="Python Data Types Explained",
            content="Overview of built-in data types in Python.",
            created_at=now - timedelta(days=10),
            tags=[python, basics]
        ),
        Article(
            title="Getting Started with SQLAlchemy ORM",
            content="How to model tables and relationships using SQLAlchemy ORM.",
            created_at=now - timedelta(days=11),
            tags=[python, sqlalchemy, orm]
        ),
        Article(
            title="One-to-Many vs Many-to-Many Relationships",
            content="Practical comparison of database relationships in ORM.",
            created_at=now - timedelta(days=1),
            tags=[sqlalchemy, orm, backend]
        ),
        Article(
            title="Building a Simple REST API",
            content="Designing a clean REST API using Python backend tools.",
            created_at=now - timedelta(days=54),
            tags=[python, api, backend]
        ),
        Article(
            title="Testing Python Applications",
            content="Unit tests, assertions and basic testing strategies.",
            created_at=now,
            tags=[python, testing]
        ),
        Article(
            title="Django vs FastAPI",
            content="Comparison of two popular Python backend frameworks.",
            created_at=now - timedelta(days=41),
            tags=[python, django, api, backend]
        ),
        Article(
            title="Optimizing Database Queries",
            content="How to avoid N+1 problems and improve query performance.",
            created_at=now - timedelta(days=21),
            tags=[sqlalchemy, orm, performance]
        ),
        Article(
            title="Designing Clean Backend Architecture",
            content="Separation of concerns and good backend practices.",
            created_at=now - timedelta(days=4),
            tags=[backend, performance]
        ),
        Article(
            title="Common ORM Mistakes",
            content="Typical mistakes developers make when using ORM tools.",
            created_at=now - timedelta(days=3),
            tags=[orm, sqlalchemy, testing]
        ),
    ]

    session.add_all(articles)
    session.commit()



def tags_of_article(session, title):
    """Zadanie 2a: Wyświetl tagi artykułu."""
    # TODO: Znajdź artykuł i wyswietl jego tagi
    result = session.query(Article).filter_by(title=title).first()
    if result:
        for tag in result.tags:
            print(f"Tag: {tag.name}, Artykuł: {title}")


def articles_with_tag(session, tag_name):
    """Zadanie 2b: Wyświetl artykuły z danym tagiem."""
    # TODO: Użyj Article.tags.any()
    result = session.query(Article).filter(Article.tags.any(Tag.name == tag_name)).all()
    for article in result:
        print(f"Artykuł: {article.title}, tag: {tag_name}")


def articles_with_both_tags(session, tag1, tag2):
    """Zadanie 2c: Artykuły z obydwoma tagami."""
    # TODO: Połącz dwa filtry any()
    result = session.query(Article).filter(Article.tags.any(Tag.name == tag1 ),Article.tags.any(Tag.name == tag2 )).all()
    for article in result:
        print(f"Artykuł: {article.title}, tagi: {tag1}, {tag2}")


def add_tag_to_article(session, title, tag_name):
    """Zadanie 3a: Dodaj tag do artykułu."""
    # TODO: Użyj article.tags.append(tag)
    article_result = session.query(Article).filter_by(title=title).first()
    tag = session.query(Tag).filter_by(name=tag_name).first()
    if article_result and tag:
        article_result.tags.append(tag)
        session.commit()



def remove_tag_from_article(session, title, tag_name):
    """Zadanie 3b: Usuń tag z artykułu."""
    # TODO: Użyj article.tags.remove(tag)
    article = session.query(Article).filter_by(title=title).first()
    tag_to_remove = session.query(Tag).filter_by(name=tag_name).first()
    if article and tag_to_remove:
        article.tags.remove(tag_to_remove)
        session.commit()


def replace_tags(session, title, new_tag_names):
    """Zadanie 3c: Zamień wszystkie tagi artykułu."""
    # TODO: Wyczyść tagi i dodaj nowe
    
    """    
    new_tag_names to lista stringów np. ["python", "api", "backend"]
    Tag.name.in_(lista) -> SQL: WHERE name IN ('python', 'api', 'backend')
    Pobiera wiele obiektów Tag jednym zapytaniem zamiast pętli z osobnymi query.
    article.tags = new_tags -> podmienia całą listę tagów na raz
    (nie trzeba clear() + append(), wystarczy przypisanie nowej listy)
    """

    article = session.query(Article).filter_by(title=title).first()
    if article:
        new_tags = session.query(Tag).filter(Tag.name.in_(new_tag_names)).all()
        article.tags = new_tags # tak albo tak jak poniżej:
        """ article.tags.clear()           # 1. usuń wszystkie stare
            article.tags.extend(new_tags)  # 2. dodaj nowe
            session.commit()
        """
        session.commit()


def count_articles_per_tag(session):
    """Zadanie 4a: Policz artykuły na tag."""
    # TODO: Użyj func.count() z group_by
    result = (session.query(
        Tag.name, func.count(Article.id).label("art_count"))
        .join(article_tag) #Zasada: N:M join = zawsze przez tabelę asocjacyjną: .join(article_tag).join(Article).
        .join(Article).
        group_by(Tag.name)
        .all())
    
    for name, art_count in result:
        print(f"{name}, {art_count}")


def most_popular_tag(session):
    """Zadanie 4b: Najpopularniejszy tag."""
    result = (
        session.query(Tag.name, func.count(Article.id).label("art_count"))
        .join(article_tag).join(Article)
        .group_by(Tag.name)
        .order_by(desc(func.count(Article.id)))
        .limit(1)
        .first()
    )
    if result:
        name, count = result
        print(f"Najpopularniejszy tag: {name} ({count} artykułów)")



def articles_without_tags(session):
    """Zadanie 4c: Artykuły bez tagow."""
    # TODO: Użyj ~Article.tags.any()
    result = session.query(Article).filter(~Article.tags.any()).all()
    for article in result:
        print(article.title)


if __name__ == "__main__":
    create_tables()

    with SessionLocal() as session:
        try:
            clear_tables(session)
            seed_data(session)
            print("\n")
            tags_of_article(session, "Common ORM Mistakes")
            print("\n")
            articles_with_tag(session, "api")
            print("\n")
            articles_with_both_tags(session, "api", "backend")
            print("\n")
            add_tag_to_article(session, "Common ORM Mistakes", "api")
            print("\n")
            remove_tag_from_article(session, "Common ORM Mistakes", "api")
            print("\n")
            replace_tags(session, "Common ORM Mistakes", ["testing","orm","performance"])
            print("\n")
            count_articles_per_tag(session)
            print("\n")
            most_popular_tag(session)
            print("\n")
            articles_without_tags(session)
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Błąd bazy danych: {e}")
