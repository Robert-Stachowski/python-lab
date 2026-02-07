from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

# TODO: Pobierz DATABASE_URL z .env
# TODO: Utworz engine
# TODO: Utworz SessionLocal
# TODO: Utworz Base

# Base = declarative_base()


# TODO: Zaimplementuj funkcje get_db() jako dependency dla FastAPI
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
