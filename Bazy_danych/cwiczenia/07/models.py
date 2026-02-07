from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


# TODO: Zdefiniuj model Student
# Kolumny: id, name, email
# Relacje: grades (1:N)

class Student(Base):
    __tablename__ = "students"

    # Tutaj zdefiniuj kolumny i relacje
    pass


# TODO: Zdefiniuj model Course
# Kolumny: id, name, instructor
# Relacje: grades (1:N)

class Course(Base):
    __tablename__ = "courses"

    # Tutaj zdefiniuj kolumny i relacje
    pass


# TODO: Zdefiniuj model Grade (tabela posrednia z danymi)
# Kolumny: id, value, date, student_id (FK), course_id (FK)
# Relacje: student, course (back_populates)

class Grade(Base):
    __tablename__ = "grades"

    # Tutaj zdefiniuj kolumny i relacje
    pass
