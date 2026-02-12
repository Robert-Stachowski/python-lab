from models import Base, Author, Book
from db import engine, SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from sqlalchemy import func, desc


def create_tables():
    """Tworzy tabele w bazie danych."""
    Base.metadata.create_all(engine)


def clear_tables(session):
    create_tables()
    session.query(Book).delete() 
    session.query(Author).delete()
    session.commit()



def seed_data(session):
    """Zadanie 1: Dodaj autorow z ksiazkami."""
    
    authors = [
        Author(
            name="George Orwell",
            country="United Kingdom",
            written_books=[
                Book(title="1984", year=1949),
                Book(title="Animal Farm", year=1945),
            ],
        ),
        Author(
            name="J.R.R. Tolkien",
            country="United Kingdom",
            written_books=[
                Book(title="The Hobbit", year=1937),
                Book(title="The Fellowship of the Ring", year=1954),
                Book(title="The Two Towers", year=1954),
                Book(title="The Return of the King", year=1955),
            ],
        ),
        Author(
            name="Haruki Murakami",
            country="Japan",
            written_books=[
                Book(title="Norwegian Wood", year=1987),
                Book(title="Kafka on the Shore", year=2002),
            ],
        ),
        Author(
            name="Frank Herbert",
            country="United States",
            written_books=[
                Book(title="Dune", year=1965),
                Book(title="Dune Messiah", year=1969),
            ],
        ),
        Author(
            name="Stanisław Lem",
            country="Poland",
            written_books=[
                Book(title="Solaris", year=1961),
                Book(title="The Cyberiad", year=1965),
            ],
        ),
    ]

    session.add_all(authors)
    session.commit()



def books_by_author(session, author_name):
    """Zadanie 2a: Wyświetl książki danego autora."""
    # TODO: Znajdź autora i wyświetl jego książki przez relacje

    # WERSJA B: Zapytanie z JOIN (bardziej "SQL-owe")
    books = session.query(Book).join(Author).filter(Author.name==author_name).all()
    if books:
        for book in books:
            print(book.title, author_name)
    else:
        print("Brak autora")


    # WERSJA A: Użycie relacji (bardziej "Pythonowe")
    author = session.query(Author).filter_by(name=author_name).first()
    if author:
        for book in author.written_books:
            print(book.title, author_name)
    else:
        print("Brak autora")
    

def author_of_book(session, book_title):
    """Zadanie 2b: Wyswietl autora danej książki."""
    # TODO: Znajdź książkę i wyświetl jej autora
    result = session.query(Book).filter_by(title=book_title).first()
    if result:
        print(book_title, result.book_author.name)
    else:
        print("Nie znaleziono książki")


def books_with_eager_loading(session):
    """Zadanie 2c: Użyj selectinload do pobrania autorow z ksiazkami."""
    # TODO: Użyj selectinload(Author.books)
    result = session.query(Author).options(selectinload(Author.written_books)).all()
    for author in result:
        titles = [book.title for book in author.written_books]
        print(f"{author.name} książki: {', '.join(titles)}")


def count_books_per_author(session):
    """Zadanie 3a: Policz książki każdego autora."""
    # TODO: Użyj func.count() z group_by()
    result = session.query(Author, func.count(Book.id).label("book_count")).join(Book).group_by(Author.id, Author.name).all()
    for author, book_count in result:
        print(f"{author.name}: {book_count} książek")


def author_with_most_books(session):
    """Zadanie 3b: Znajdź autora z najwieksza liczba ksiazek."""
    # TODO: Użyj having() lub order_by z limit
    result = (
        session.query(Author, func.count(Book.id).label("book_count"))
        .join(Book)
        .group_by(Author.id, Author.name)
        .order_by(desc(func.count(Book.id)))
        .first())
    
    if result:
        author, book_count = result
        print(f"{author.name}: {book_count} książek")
    else:
        print("Brak wyników")   
        


def avg_year_per_author(session):
    """Zadanie 3c: Średni rok wydania na autora."""
    # TODO: Użyj func.avg()
    result = (
        session.query(Author, func.avg(Book.year).label("avg_year"))
        .join(Book)
        .group_by(Author.id, Author.name)
        .all())
    for author, avg_year in result:
        print(f"{author.name}, wynik: {avg_year:.2f}")





def delete_author_cascade(session, author_name):
    """Zadanie 4: Usuń autora kaskadowo."""
    # TODO: Usuń autora i sprawdz czy książki tez znikły
    
    author = session.query(Author).filter_by(name=author_name).first()
    if not author:
        print("nie znaleziono autora")
        return
    
    print(f"\n=== PRZED USUNIĘCIEM ===")
    for book in author.written_books:
        print(f"Autor: {author_name}, książki {book.title}")

    author_id = author.id  # Zachowaj ID przed usunięciem

    session.delete(author)
    session.commit()

    result_after = session.query(Book).filter(Book.author_id==author_id).all() #używamy zapisanego author_id przed usunieciem
    if result_after:
        print(f"Ups, pozostały książki: {[book.title for book in result_after]}")
    else:
        print("\nGitara, autor i książki usunięte")



if __name__ == "__main__":
    create_tables()

    with SessionLocal() as session:
        try:
            clear_tables(session)
            seed_data(session)
            print("\n")
            books_by_author(session, "Stanisław Lem")
            print("\n")
            author_of_book(session, "The Hobbit")
            print("\n")
            books_with_eager_loading(session)
            print("\n")
            count_books_per_author(session)
            print("\n")
            author_with_most_books(session)
            print("\n")
            avg_year_per_author(session)
            print("\n")
            delete_author_cascade(session, "Stanisław Lem")

        except SQLAlchemyError as e:
            session.rollback()
            print(f"Błąd bazy danych: {e}")
