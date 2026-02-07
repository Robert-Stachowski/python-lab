from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


# TODO: Zdefiniuj tabele asocjacyjna article_tag
# Uzyj Table() z dwoma kolumnami: article_id i tag_id
# Obie kolumny to ForeignKey i razem tworza Primary Key

# article_tag = Table(...)


# TODO: Zdefiniuj model Article
# Kolumny: id, title, content, created_at
# Relacja: tags (N:M przez article_tag)

class Article(Base):
    __tablename__ = "articles"

    # Tutaj zdefiniuj kolumny i relacje
    pass


# TODO: Zdefiniuj model Tag
# Kolumny: id, name (UNIQUE)
# Relacja: articles (N:M przez article_tag)

class Tag(Base):
    __tablename__ = "tags"

    # Tutaj zdefiniuj kolumny i relacje
    pass
