from models import Base, Workout
from db import engine, SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from datetime import date, timedelta


def create_tables():
    """Tworzy tabele w bazie danych."""
    Base.metadata.create_all(engine)


def seed_workouts(session):
    """Zadanie 1: Dodaj co najmniej 10 treningow."""
    # TODO: Utworz obiekty Workout z roznymi typami i datami
    pass


def filter_by_type(session, workout_type):
    """Zadanie 2a: Znajdz treningi danego typu."""
    # TODO: Uzyj filter_by lub filter
    pass


def filter_by_duration(session, min_minutes):
    """Zadanie 2b: Znajdz treningi dluzsze niz min_minutes."""
    # TODO: Uzyj filter z operatorem >
    pass


def filter_last_7_days(session):
    """Zadanie 2c: Znajdz treningi z ostatnich 7 dni."""
    # TODO: Uzyj date.today() - timedelta(days=7)
    pass


def sort_by_date(session):
    """Zadanie 3a: Sortuj po dacie malejaco."""
    # TODO: Uzyj order_by z desc()
    pass


def sort_by_calories(session):
    """Zadanie 3b: Sortuj po kaloriach malejaco."""
    # TODO: Uzyj order_by z desc()
    pass


def sort_by_duration(session):
    """Zadanie 3c: Sortuj po czasie trwania rosnaco."""
    # TODO: Uzyj order_by
    pass


def strength_over_45_sorted(session):
    """Zadanie 4a: Treningi sila > 45 min, posortowane po dacie."""
    # TODO: Polacz filter i order_by
    pass


def top_3_longest_cardio(session):
    """Zadanie 4b: 3 najdluzsze treningi cardio."""
    # TODO: Polacz filter, order_by i limit
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
