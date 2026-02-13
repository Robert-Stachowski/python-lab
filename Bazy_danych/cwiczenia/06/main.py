from models import Base, Movie
from db import engine, SessionLocal
from sqlalchemy.exc import SQLAlchemyError
import math
from sqlalchemy import func, between, desc


def create_tables():
    """Tworzy tabelę w bazie danych."""
    Base.metadata.create_all(engine)

def clear_table(session):
    create_tables()
    session.query(Movie).delete()
    session.commit()



def seed_movies(session):
    """Zadanie 1: Dodaj co najmniej 25 filmów."""
    # TODO: Utwórz listę filmów i dodaj do bazy
    movies = [
        Movie(title="Inception", director="Christopher Nolan", year=2010, genre="Sci-Fi", rating=8.8),
        Movie(title="Interstellar", director="Christopher Nolan", year=2014, genre="Sci-Fi", rating=8.6),
        Movie(title="The Dark Knight", director="Christopher Nolan", year=2008, genre="Action", rating=9.0),

        Movie(title="Pulp Fiction", director="Quentin Tarantino", year=1994, genre="Crime", rating=8.9),
        Movie(title="Django Unchained", director="Quentin Tarantino", year=2012, genre="Western", rating=8.4),
        Movie(title="Once Upon a Time in Hollywood", director="Quentin Tarantino", year=2019, genre="Drama", rating=7.6),

        Movie(title="The Godfather", director="Francis Ford Coppola", year=1972, genre="Crime", rating=9.2),
        Movie(title="The Godfather Part II", director="Francis Ford Coppola", year=1974, genre="Crime", rating=9.0),

        Movie(title="Fight Club", director="David Fincher", year=1999, genre="Drama", rating=8.8),
        Movie(title="Se7en", director="David Fincher", year=1995, genre="Thriller", rating=8.6),
        Movie(title="Gone Girl", director="David Fincher", year=2014, genre="Thriller", rating=8.1),

        Movie(title="The Matrix", director="Lana Wachowski", year=1999, genre="Sci-Fi", rating=8.7),
        Movie(title="The Matrix Reloaded", director="Lana Wachowski", year=2003, genre="Sci-Fi", rating=7.2),

        Movie(title="Gladiator", director="Ridley Scott", year=2000, genre="Historical", rating=8.5),
        Movie(title="Blade Runner", director="Ridley Scott", year=1982, genre="Sci-Fi", rating=8.1),
        Movie(title="Alien", director="Ridley Scott", year=1979, genre="Horror", rating=8.5),

        Movie(title="The Shawshank Redemption", director="Frank Darabont", year=1994, genre="Drama", rating=9.3),
        Movie(title="The Green Mile", director="Frank Darabont", year=1999, genre="Drama", rating=8.6),

        Movie(title="Forrest Gump", director="Robert Zemeckis", year=1994, genre="Drama", rating=8.8),
        Movie(title="Back to the Future", director="Robert Zemeckis", year=1985, genre="Sci-Fi", rating=8.5),

        Movie(title="Parasite", director="Bong Joon-ho", year=2019, genre="Thriller", rating=8.6),
        Movie(title="Memories of Murder", director="Bong Joon-ho", year=2003, genre="Crime", rating=8.1),

        Movie(title="Whiplash", director="Damien Chazelle", year=2014, genre="Drama", rating=8.5),
        Movie(title="La La Land", director="Damien Chazelle", year=2016, genre="Musical", rating=8.0),

        Movie(title="Mad Max: Fury Road", director="George Miller", year=2015, genre="Action", rating=8.1),
    ]

    session.add_all(movies)
    session.commit()



def get_page(session, page, per_page=5):
    """Zadanie 2: Pobierz filmy z danej strony."""
    # TODO: Oblicz offset, użyj limit i offset
    # TODO: Oblicz łączną liczbe stron

    total = session.query(func.count(Movie.id)).scalar()
    total_pages = math.ceil(total / per_page)
    print(f"--- Strona {page} z {total_pages} (łącznie {total} filmow) ---")

    offset = (page - 1) * per_page
    result = session.query(Movie).offset(offset).limit(per_page).all()
    for movie in result:
        print(f"{movie.title} ({movie.year}) - {movie.genre} - {movie.rating}")
    


def search_by_title(session, fragment):
    """Zadanie 3a: Wyszukaj po fragmencie tytułu."""
    # TODO: Użyj ilike("%fragment%")
    result = session.query(Movie).filter(Movie.title.ilike(f"%{fragment}%")).all()
    for movie in result:
        print(f" Tytuł filmu: {movie.title}, Wyszukany po fragmencie: '{fragment}'")


def search_by_director(session, director_name):
    """Zadanie 3b: Wyszukaj po reżyserze."""
    # TODO: Użyj ilike
    result = session.query(Movie).filter(Movie.director.ilike(f"%{director_name}%")).all()
    print(f"Rezyser: '{director_name}', filmy: ")
    for movie in result:
        print(f"{movie.title}")


def search_by_genre_and_years(session, genre, year_from, year_to):
    """Zadanie 3c: Wyszukaj po gatunku i zakresie lat."""
    # TODO: Użyj filter z between()
    result = (
        session.query(Movie)
        .filter(Movie.genre==genre)
        .filter(Movie.year.between(year_from, year_to))
        .all())
    for movie in result:
        print(f"Gatunek: {genre}, filmy: {movie.title} ({movie.year})")


def search_movies(session, query, page=1, per_page=3):
    """Zadanie 4: Wyszukiwanie z paginacja."""
    # TODO: Połącz ilike z offset/limit
    total = session.query(func.count(Movie.id)).filter(Movie.title.ilike(f"%{query}%")).scalar()
    total_pages = math.ceil(total / per_page)
    print(f"---  Wyszukiwanie z paginacją: '{query}' ,strona {page} / {total_pages}  ---")

    offset = (page - 1) * per_page
    result = session.query(Movie).filter(Movie.title.ilike(f"%{query}%")).offset(offset).limit(per_page).all()
    for movie in result:
        print(f"{movie.title} ({movie.year}) - {movie.genre} - {movie.rating}")


def sorted_page(session, sort_by="rating", page=1, per_page=5):
    """Zadanie 5: Sortowanie z paginacja."""
    # TODO: Połącz order_by z offset/limit
    
    #Mapowanie stringa na kolumnę:
    #od razu mapujemy inne stringi po których można sortować
    columns = {
        "rating" : Movie.rating,
        "year" : Movie.year,
        "title" : Movie.title
    }

    sort_columns = columns.get(sort_by, Movie.rating) #wybieramy sortowanie po rating

    offset = (page -1) *per_page
    result = session.query(Movie).order_by(desc(sort_columns)).offset(offset).limit(per_page).all()
    for movie in result:
        print(f"{movie.title} ({movie.year}) - {movie.rating}")

    


if __name__ == "__main__":
    create_tables()

    with SessionLocal() as session:
        try:
            clear_table(session)
            seed_movies(session)
            print("\n")
            get_page(session, 1, per_page=5)
            print("\n")
            search_by_title(session, "ma")
            print("\n")
            search_by_director(session, "Ridley Scott")
            print("\n")
            search_by_genre_and_years(session, "Drama", 1982, 2005)
            print("\n")
            search_movies(session, "the", page=1, per_page=3)
            print("\n")
            sorted_page(session, page=1, per_page=5)
            print("\n")
            sorted_page(session, sort_by="year", page=1, per_page=5)

        except SQLAlchemyError as e:
            session.rollback()
            print(f"Błąd bazy danych: {e}")
