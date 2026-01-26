import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is missing. Check your .env file.")

engine = create_engine(DATABASE_URL, echo=False, future=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

if __name__ == "__main__":
    try:
        with SessionLocal() as session:
            session.execute(text("SELECT 1"))
            print("OK: Database connection works")
    except Exception as e:
        print("FAILED: Database connection")
        raise
