from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


# TODO: Zdefiniuj model Student
# Kolumny: id, name, email
# Relacje: grades (1:N)

class Student(Base):
    __tablename__ = "students"

    id  = Column(Integer, primary_key=True)
    name = Column(String(length=100), nullable=False)
    email = Column(String(length=100), nullable=False, unique=True)

    grades = relationship("Grade", back_populates="student", cascade="all, delete-orphan")


# TODO: Zdefiniuj model Course
# Kolumny: id, name, instructor
# Relacje: grades (1:N)

class Course(Base):
    __tablename__ = "courses"

    id  = Column(Integer, primary_key=True)
    name = Column(String(length=100), nullable=False)
    instructor = Column(String(length=100), nullable=False)

    grades = relationship("Grade", back_populates="course", cascade="all, delete-orphan")



# TODO: Zdefiniuj model Grade (tabela posrednia z danymi)
# Kolumny: id, value, date, student_id (FK), course_id (FK)
# Relacje: student, course (back_populates)

class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True)
    value = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))

    student = relationship("Student", back_populates="grades")
    course = relationship("Course", back_populates="grades")