from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()



article_tag = Table(
    "article_tag",
    Base.metadata,
    Column("article_id", Integer, ForeignKey("articles.id"), primary_key = True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True)
)



class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(length=100), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    tags = relationship("Tag", secondary="article_tag", back_populates="articles")



class Tag(Base):
    __tablename__ = "tags"

    id =Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=50), nullable=False, unique=True)

    articles = relationship("Article", secondary="article_tag", back_populates="tags")