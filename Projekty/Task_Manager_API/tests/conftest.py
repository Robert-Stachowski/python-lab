import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.database import Base, get_db

# TODO: Zaimportuj app, Base, get_db

# TODO: Skonfiguruj testowa baze danych (SQLite in-memory)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(bind=engine)


# TODO: Zdefiniuj fixture ktora nadpisuje get_db
@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


# TODO: Zdefiniuj fixture dla TestClient
@pytest.fixture
def client(db):
    def override_get_db():
        yield db
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(client):
    response = client.post("/users/", json={
        "username": "test_data_username",
        "email": "example@exapmle.pl"
    })
    return response.json()


@pytest.fixture
def test_project(client, test_user):
    response = client.post("/projects/", json={
        "name": "Test projekt numer jeden. ",
        "description": "Opis projektu. ",
        "owner_id": test_user["id"]
    })
    return response.json()
