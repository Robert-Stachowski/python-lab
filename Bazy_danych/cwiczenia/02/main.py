from models import Base, Workout
from db import engine, SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from datetime import date, timedelta
from sqlalchemy import desc


def create_tables():
    """Tworzy tabele w bazie danych."""
    Base.metadata.create_all(engine)

def clear_table_workout(session):
    create_tables()
    session.query(Workout).delete()
    session.commit()


def seed_workouts(session):
    """Zadanie 1: Dodaj co najmniej 10 treningow."""
    now = date.today()
    workouts = [
        Workout(
            name="Morning Run",
            workout_type="Cardio",
            duration_minutes=45,
            calories=420,
            date=date(2026, 2, 1)
        ),
        Workout(
            name="Evening Gym",
            workout_type="Strength",
            duration_minutes=70,
            calories=550,
            date=now - timedelta(days=2)
        ),
        Workout(
            name="Core Blast",
            workout_type="Strength",
            duration_minutes=30,
            calories=260,
            date=now - timedelta(days=1)
        ),
        Workout(
            name="Full Body Burn",
            workout_type="HIIT",
            duration_minutes=40,
            calories=480,
            date=now - timedelta(days=3)
        ),
        Workout(
            name="Leg Day",
            workout_type="Strength",
            duration_minutes=75,
            calories=620,
            date=now - timedelta(days=3)
        ),
        Workout(
            name="Upper Power",
            workout_type="Strength",
            duration_minutes=60,
            calories=500,
            date=now - timedelta(days=6)
        ),
        Workout(
            name="HIIT Express",
            workout_type="HIIT",
            duration_minutes=25,
            calories=300,
            date=now - timedelta(days=4)
        ),
        Workout(
            name="Mobility Flow",
            workout_type="Mobility",
            duration_minutes=35,
            calories=180,
            date=now - timedelta(days=2)
        ),
        Workout(
            name="Endurance Ride",
            workout_type="Endurance",
            duration_minutes=90,
            calories=750,
            date=now - timedelta(days=1)
        ),
        Workout(
            name="Recovery Walk",
            workout_type="Cardio",
            duration_minutes=50,
            calories=220,
            date=now
        ),
    ]

    session.add_all(workouts)
    session.commit()



def filter_by_type(session, workout_type):
    """Zadanie 2a: Znajdz treningi danego typu."""
    # TODO: Użyj filter_by lub filter
    results = session.query(Workout).filter_by(workout_type=workout_type).all()
    for result in results:
        print(result.workout_type, result.name)


def filter_by_duration(session, min_minutes):
    """Zadanie 2b: Znajdź treningi dłuższe niz min_minutes."""
    # TODO: Użyj filter z operatorem >
    results = session.query(Workout).filter(Workout.duration_minutes>min_minutes).all()
    for result in results:
        print(result.name, result.duration_minutes, min_minutes)


def filter_last_7_days(session):
    """Zadanie 2c: Znajdź treningi z ostatnich 7 dni."""
    # TODO: Uzyj date.today() - timedelta(days=7)
    results = session.query(Workout).filter(Workout.date >= date.today()-timedelta(days=7)).all()
    for result in results:
        print(result.name, result.date)


def sort_by_date(session):
    """Zadanie 3a: Sortuj po dacie malejąco."""
    # TODO: Uzyj order_by z desc()
    results =session.query(Workout).order_by(desc(Workout.date)).all()
    for result in results:
        print(result.name, result.date)


def sort_by_calories(session):
    """Zadanie 3b: Sortuj po kaloriach malejaco."""
    # TODO: Uzyj order_by z desc()
    results = session.query(Workout).order_by(desc(Workout.calories)).all()
    for result in results:
        print(result.name, result.calories)


def sort_by_duration(session):
    """Zadanie 3c: Sortuj po czasie trwania rosnaco."""
    # TODO: Użyj order_by
    results = session.query(Workout).order_by(Workout.duration_minutes).all()
    for result in results:
        print(result.name, result.duration_minutes)


def strength_over_45_sorted(session):
    """Zadanie 4a: Treningi sila > 45 min, posortowane po dacie."""
    # TODO: Połącz filter i order_by
    results = session.query(Workout).filter_by(workout_type="Strength").filter(Workout.duration_minutes>45).order_by(Workout.date).all()
    for result in results:
        print(result.name, result.duration_minutes, result.date)


def top_3_longest_cardio(session):
    """Zadanie 4b: 3 najdłuższe treningi cardio."""
    # TODO: Połącz filter, order_by i limit
    results = session.query(Workout).filter(Workout.workout_type=="Cardio").order_by(desc(Workout.duration_minutes)).limit(3).all()
    for result in results:
        print(result.name, result.workout_type, result.duration_minutes)


if __name__ == "__main__":
    create_tables()

    with SessionLocal() as session:
        try:
            clear_table_workout(session)
            print("\n")
            seed_workouts(session)
            print("\n")
            filter_by_type(session, "Strength")
            print("\n")
            filter_by_duration(session, 60)
            print("\n")
            filter_last_7_days(session)
            print("\n")
            sort_by_date(session)
            print("\n")
            sort_by_calories(session)
            print("\n")
            sort_by_duration(session)
            print("\n")
            strength_over_45_sorted(session)
            print("\n")
            top_3_longest_cardio(session)            


        except SQLAlchemyError as e:
            session.rollback()
            print(f"Błąd bazy danych: {e}")
