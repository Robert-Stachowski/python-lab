from models import Base, Student, Course, Grade
from db import engine, SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from datetime import date


def create_tables():
    """Tworzy tabele w bazie danych."""
    Base.metadata.create_all(engine)


def seed_data(session):
    """Zadanie 1: Dodaj uczniow, kursy i oceny."""
    # TODO: Utworz uczniow, kursy, a potem oceny laczace ich
    pass


def student_grades(session, student_name):
    """Zadanie 2a: Oceny danego ucznia."""
    # TODO: Znajdz ucznia i wyswietl jego oceny z nazwami kursow
    pass


def students_in_course(session, course_name):
    """Zadanie 2b: Uczniowie na danym kursie."""
    # TODO: Znajdz kurs i wyswietl uczniow
    pass


def course_grades_sorted(session, course_name):
    """Zadanie 2c: Oceny z kursu posortowane."""
    # TODO: Uzyj join i order_by
    pass


def avg_grade_per_student(session):
    """Zadanie 3a: Srednia ocen kazdego ucznia."""
    # TODO: Uzyj func.avg z group_by
    pass


def avg_grade_per_course(session):
    """Zadanie 3b: Srednia ocen na kursie."""
    # TODO: Uzyj func.avg z group_by
    pass


def best_student(session):
    """Zadanie 3c: Uczen z najwyzsza srednia."""
    # TODO: Uzyj order_by(desc) z limit(1)
    pass


def worst_course(session):
    """Zadanie 3d: Kurs z najnizsza srednia."""
    # TODO: Uzyj order_by(asc) z limit(1)
    pass


def students_with_low_grades(session, threshold=3.0):
    """Zadanie 4a: Uczniowie z ocena ponizej progu."""
    # TODO: Uzyj join z filter
    pass


def student_ranking(session):
    """Zadanie 4b: Ranking uczniow po sredniej."""
    # TODO: Uzyj func.avg z group_by i order_by
    pass


def grades_per_month(session):
    """Zadanie 4c: Liczba ocen na miesiac."""
    # TODO: Uzyj func.strftime('%m', Grade.date) dla SQLite
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
