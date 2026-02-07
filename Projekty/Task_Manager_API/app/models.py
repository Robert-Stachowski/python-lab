from sqlalchemy import Column, Integer, String, Text, Boolean, Float, Date, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime

# TODO: Zaimportuj Base z database.py
# from .database import Base


# TODO: Zdefiniuj tabele asocjacyjna task_tag
# task_tag = Table(...)


# TODO: Zdefiniuj model User
# Kolumny: id, username (UNIQUE), email (UNIQUE), is_active, created_at
# Relacje: projects (1:N), assigned_tasks (1:N)

# class User(Base):
#     __tablename__ = "users"
#     pass


# TODO: Zdefiniuj model Project
# Kolumny: id, name, description, owner_id (FK), created_at
# Relacje: owner (User), tasks (1:N, cascade)

# class Project(Base):
#     __tablename__ = "projects"
#     pass


# TODO: Zdefiniuj model Task
# Kolumny: id, title, description, status, priority, due_date,
#          created_at, updated_at, project_id (FK), assignee_id (FK, nullable)
# Relacje: project, assignee (User), tags (N:M)

# class Task(Base):
#     __tablename__ = "tasks"
#     pass


# TODO: Zdefiniuj model Tag
# Kolumny: id, name (UNIQUE)
# Relacja: tasks (N:M)

# class Tag(Base):
#     __tablename__ = "tags"
#     pass
