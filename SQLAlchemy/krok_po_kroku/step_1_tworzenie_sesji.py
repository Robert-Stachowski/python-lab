from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# wczytuje zmienne z pliku .env
load_dotenv()

# =========================
# DATABASE_URL — 3 warianty 
# =========================

# 1) SQLite (lokalny plik)
# DATABASE_URL=sqlite:///mydatabase.db

# 2) PostgreSQL lokalny
# DATABASE_URL=postgresql+psycopg://postgres@localhost:5432/mojabaza

# 3) PostgreSQL zdalny (często SSL)
# DATABASE_URL=postgresql+psycopg://user@db.example.com:5432/mojabaza?sslmode=require

# =========================
# AKTYWNY WYBÓR Z .env
# =========================
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


