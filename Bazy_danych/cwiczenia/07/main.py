from models import Base, Student, Course, Grade
from db import engine, SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, desc, asc
from datetime import datetime, timedelta


def create_tables():
    """Tworzy tabele w bazie danych."""
    Base.metadata.create_all(engine)

def clear_all_tables(session):
    create_tables()
    session.query(Grade).delete()
    session.query(Course).delete()
    session.query(Student).delete()
    session.commit()


def seed_data(session):
    """Zadanie 1: Dodaj uczniów, kursy i oceny."""
    # TODO: Utwórz uczniów, kursy, a potem oceny łączące ich
    now = datetime.utcnow()


    Cooking = Course(name = "Gotowanie", instructor = "Nikodem Pląs")
    Something = Course(name = "Dziewiarstwo", instructor = "Celina Orłowska")
    programming = Course(name = "Klepanie kodu", instructor = "Gabriel Altshift")
    
    
    
    students = [
        Student(
            name = "Michał Jarzyna",
            email = "jarzynaM@example.pl",
            grades=[
                Grade(value=3.0, date = now - timedelta(days=2), course = Cooking ),
                Grade(value=6.0, date = now - timedelta(days=5), course = Something )
            ]
            
            ),
        Student(
            name = "Zofia Naukowska",
            email = "naukowskaZo@example.pl",
            grades=[
                Grade(value=4.5, date = now - timedelta(days=2), course = Cooking ),
                Grade(value=3.0, date = now - timedelta(days=5), course = programming )
            ]
        ),
        Student(
            name = "Zenon Burczymucha",
            email = "BurczyZenek@example.pl",
            grades=[
                Grade(value=4.0, date = now - timedelta(days=13), course = Cooking ),
                Grade(value=4.0, date = now - timedelta(days=3), course = Something ),
                Grade(value=4.0, date = now, course = programming )
            ]
        ),
        Student(
            name = "Gracjan Nieroztocki",
            email = "NieGracek@example.pl",
            grades=[                
                Grade(value=6.0, date = now, course = Something ),
                Grade(value=3.5, date = now - timedelta(days=30), course = programming )
            ]
        ),
        Student(
            name = "Karol Nadwiślany",
            email = "WisłaKarok@example.pl",
            grades=[
                Grade(value=5.0, date = now - timedelta(days=4), course = Cooking ),
                Grade(value=6.0, date = now - timedelta(days=1), course = Something ),
                Grade(value=4.5, date = now - timedelta(days=3), course = programming )
            ]
        )
    ]

    session.add_all([Cooking, Something, programming, *students]) # *rozpakowujemy listę 
    session.commit()    
    




def student_grades(session, student_name):
    """Zadanie 2a: Oceny danego ucznia."""
    # TODO: Znajdz ucznia i wyświetl jego oceny z nazwami kursów
    result = session.query(Grade).join(Student).filter(Student.name==student_name).all()
    print(f"--- Oceny ucznia: {student_name} ---")
    for grade in result:
        print(f"{grade.course.name}, {grade.value}, {grade.date}")


def students_in_course(session, course_name):
    """Zadanie 2b: Uczniowie na danym kursie."""
    # TODO: Znajdź kurs i wyświetl uczniów
    result = session.query(Student).join(Grade).join(Course).filter(Course.name==course_name).all()
    print(f"--- Uczniowie na kursie: {course_name} ---")
    for student in result:
        print(f"{student.name} ")


def course_grades_sorted(session, course_name):
    """Zadanie 2c: Oceny z kursu posortowane."""
    # TODO: Użyj join i order_by
    result = session.query(Grade).join(Course).filter(Course.name==course_name).order_by(desc(Grade.value)).all()
    for grade in result:
        print(f"{grade.student.name}: ({grade.value})")


def avg_grade_per_student(session):
    """Zadanie 3a: Średnia ocen każdego ucznia."""
    # TODO: Użyj func.avg z group_by
    result = (
        session.query(Student.name, func.avg(Grade.value))
        .join(Student)
        .group_by(Student.name)
        .order_by(desc(func.avg(Grade.value)))
        .all()
        )
    print("--- Ranking uczniów ---")
    for student, avg in result:
        print(f"{student} - średnia: {avg}")


def avg_grade_per_course(session):
    """Zadanie 3b: Średnia ocen na kursie."""
    # TODO: Użyj func.avg z group_by
    result = session.query(Course.name, func.avg(Grade.value)).join(Course).group_by(Course.name).all()
    print("--- Średnia ocen na kursie: ---")
    for course, avg in result:
        print(f"{course} : ({avg})")


def best_student(session):
    """Zadanie 3c: Uczeń z najwyższą średnią."""
    # TODO: Użyj order_by(desc) z limit(1)
    result = (
        session.query(Student.name, func.avg(Grade.value))
        .join(Student)
        .group_by(Student.name)
        .order_by(desc(func.avg(Grade.value)))
        .limit(1)
        .first()
        )
    print("--- Uczeń z największą średnią: ---") 
    if result:
        name, avg = result
        print(f"{name} : ({avg:.2f})")


def worst_course(session):
    """Zadanie 3d: Kurs z najniższą średnią."""
    # TODO: Użyj order_by(asc) z limit(1)
    result = (
        session.query(Course.name, func.avg(Grade.value))
        .join(Course)
        .group_by(Course.name)
        .order_by(asc(func.avg(Grade.value)))
        .limit(1)
        .first()
        )
    print("--- Kurs z najniższą średnią: ---") 
    if result:
        name, avg = result
        print(f"{name} : ({avg:.2f})")



    

def students_with_low_grades(session, threshold=3.0):
    """Zadanie 4a: Uczniowie z oceną poniżej progu."""
    # TODO: Użyj join z filter
    result = (
        session.query(Student.name, Course.name, Grade.value)
        .join(Student)
        .join(Course)
        .filter(Grade.value <= threshold)
        .all()
        )
    print(f"--- Uczniowie z oceną poniżej ({threshold}) ---")
    for name, course, value in result:
        print(f"{name}:  {value} z {course}")


def student_ranking(session):
    """Zadanie 4b: Ranking uczniów po średniej."""
    # TODO: Użyj func.avg z group_by i order_by
    result = (
        session.query(Student.name, func.avg(Grade.value))
        .join(Student)
        .group_by(Student.name)
        .order_by(desc(func.avg(Grade.value)))
        .all()
        )
    print(f"--- Ranking uczniów wg średniej oceny:  ---")
    for name, avg in result:
        print(f"{name} : {avg}")


def grades_per_month(session):
    """Zadanie 4c: Liczba ocen na miesiąc."""
    # TODO: Użyj func.strftime('%m', Grade.date) dla SQLite
    result = (
        session.query(func.strftime('%m', Grade.date), func.count(Grade.id))
        .group_by(func.strftime('%m', Grade.date))
        .order_by(func.strftime('%m', Grade.date))
        .all()
        )
    print("--- Liczba ocen na miesiąc ---")
    for month, count in result:
        print(f"Miesiąc {month}: {count} ocen")


if __name__ == "__main__":
    create_tables()

    with SessionLocal() as session:
        try:
            clear_all_tables(session)
            seed_data(session)
            student_grades(session, "Zenon Burczymucha")
            print("\n")
            students_in_course(session, "Dziewiarstwo")
            print("\n")
            course_grades_sorted(session, "Dziewiarstwo")
            print("\n")
            avg_grade_per_course(session)
            print("\n")
            avg_grade_per_student(session)
            print("\n")
            best_student(session)
            print("\n")
            worst_course(session)
            print("\n")
            students_with_low_grades(session)
            print("\n")
            student_ranking(session)
            print("\n")
            grades_per_month(session)
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Błąd bazy danych: {e}")
