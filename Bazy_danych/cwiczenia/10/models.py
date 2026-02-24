from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


# TODO: Zdefiniuj tabele asocjacyjna post_tag

post_tag = Table(
    "post_tag",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True)
)


# TODO: Zdefiniuj model User
# Kolumny: id, username, email, role, created_at
# Relacje: posts, comments

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(length=50), nullable=False, unique=True)
    email = Column(String(length=100), nullable=False, unique=True)
    role = Column(String(length=20), default="author")
    created_at = Column(DateTime, default=datetime.utcnow)

    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")


# TODO: Zdefiniuj model Category
# Kolumny: id, name, description
# Relacja: posts

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=100), nullable=False, unique=True)
    description = Column(Text)

    posts = relationship("Post", back_populates="category", cascade="all, delete-orphan")


# TODO: Zdefiniuj model Post
# Kolumny: id, title, content, is_published, created_at, updated_at, author_id, category_id
# Relacje: author, category, tags (N:M), comments (cascade)

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(length=200), nullable=False)
    content = Column(Text, nullable=False)
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    author_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))

    user = relationship("User", back_populates="posts")
    category = relationship("Category", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")

    tags = relationship("Tag", secondary="post_tag", back_populates="posts")


# TODO: Zdefiniuj model Tag
# Kolumny: id, name
# Relacja: posts (N:M)

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=50), nullable=False, unique=True)

    posts = relationship("Post", secondary="post_tag", back_populates="tags")


# TODO: Zdefiniuj model Comment
# Kolumny: id, content, created_at, author_id, post_id
# Relacje: author, post

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    author_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))

    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")