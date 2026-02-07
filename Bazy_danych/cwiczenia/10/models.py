from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


# TODO: Zdefiniuj tabele asocjacyjna post_tag

# post_tag = Table(...)


# TODO: Zdefiniuj model User
# Kolumny: id, username, email, role, created_at
# Relacje: posts, comments

class User(Base):
    __tablename__ = "users"

    # Tutaj zdefiniuj kolumny i relacje
    pass


# TODO: Zdefiniuj model Category
# Kolumny: id, name, description
# Relacja: posts

class Category(Base):
    __tablename__ = "categories"

    # Tutaj zdefiniuj kolumny i relacje
    pass


# TODO: Zdefiniuj model Post
# Kolumny: id, title, content, is_published, created_at, updated_at, author_id, category_id
# Relacje: author, category, tags (N:M), comments (cascade)

class Post(Base):
    __tablename__ = "posts"

    # Tutaj zdefiniuj kolumny i relacje
    pass


# TODO: Zdefiniuj model Tag
# Kolumny: id, name
# Relacja: posts (N:M)

class Tag(Base):
    __tablename__ = "tags"

    # Tutaj zdefiniuj kolumny i relacje
    pass


# TODO: Zdefiniuj model Comment
# Kolumny: id, content, created_at, author_id, post_id
# Relacje: author, post

class Comment(Base):
    __tablename__ = "comments"

    # Tutaj zdefiniuj kolumny i relacje
    pass
