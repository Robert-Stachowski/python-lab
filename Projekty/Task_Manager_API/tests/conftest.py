import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# TODO: Zaimportuj app, Base, get_db
# from app.main import app
# from app.database import Base, get_db

# TODO: Skonfiguruj testowa baze danych (SQLite in-memory)
# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# TestingSessionLocal = sessionmaker(bind=engine)


# TODO: Zdefiniuj fixture ktora nadpisuje get_db
# @pytest.fixture
# def db():
#     Base.metadata.create_all(bind=engine)
#     session = TestingSessionLocal()
#     try:
#         yield session
#     finally:
#         session.close()
#         Base.metadata.drop_all(bind=engine)


# TODO: Zdefiniuj fixture dla TestClient
# @pytest.fixture
# def client(db):
#     def override_get_db():
#         yield db
#     app.dependency_overrides[get_db] = override_get_db
#     with TestClient(app) as c:
#         yield c
#     app.dependency_overrides.clear()
