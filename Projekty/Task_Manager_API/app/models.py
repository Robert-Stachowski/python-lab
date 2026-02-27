from sqlalchemy import Column, Integer, String, Text, Boolean, Date, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

# TODO: Zaimportuj Base z database.py
from .database import Base


# TODO: Zdefiniuj tabele asocjacyjna task_tag
task_tag = Table(
    "task_tag",
    Base.metadata,
    Column("task_id", Integer, ForeignKey("tasks.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True)
)


# TODO: Zdefiniuj model User
# Kolumny: id, username (UNIQUE), email (UNIQUE), is_active, created_at
# Relacje: projects (1:N), assigned_tasks (1:N)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(length=50), nullable=False, unique=True)
    email = Column(String(length=100), nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")
    assigned_tasks = relationship("Task", back_populates="assignee")

# TODO: Zdefiniuj model Project
# Kolumny: id, name, description, owner_id (FK), created_at
# Relacje: owner (User), tasks (1:N, cascade)

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=100), nullable=False)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")



# TODO: Zdefiniuj model Task
# Kolumny: id, title, description, status, priority, due_date,
#          created_at, updated_at, project_id (FK), assignee_id (FK, nullable)
# Relacje: project, assignee (User), tags (N:M)

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(length=200), nullable=False)
    description = Column(Text)
    status = Column(String(length=20), default="todo" )#(todo/in_progress/done)
    priority = Column(String(length=20), default="medium" )#(low/medium/high/critical)
    due_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    assignee_id = Column(Integer, ForeignKey("users.id"))

    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User", back_populates="assigned_tasks")

    tags = relationship("Tag", secondary="task_tag", back_populates="tasks")


# TODO: Zdefiniuj model Tag
# Kolumny: id, name (UNIQUE)
# Relacja: tasks (N:M)

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=50), nullable=False, unique=True)

    tasks = relationship("Task", secondary="task_tag", back_populates="tags")

