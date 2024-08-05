from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from app.app import app
from app.database import Base, get_db

DATABASE_URL = "sqlite:///./test_weather.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


# Dependency override
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_and_teardown():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_add_weather_data():
    response = client.post(
        "/weather/",
        json={
            "city": "New York",
            "temperature": 22.5,
            "description": "Sunny",
            "date": "2022-01-01",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["city"] == "New York"
    assert data["temperature"] == 22.5
    assert data["description"] == "Sunny"
    assert data["date"] == "2022-01-01"


def test_add_duplicate_city():
    # add city the first time
    client.post(
        "/weather/",
        json={
            "city": "New York",
            "temperature": 22.5,
            "description": "Sunny",
            "date": "2022-01-01",
        },
    )

    # add city the second time
    response = client.post(
        "/weather/",
        json={
            "city": "New York",
            "temperature": 22.5,
            "description": "Sunny",
            "date": "2022-01-01",
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "City already exist"}


def test_get_weather_data():
    client.post(
        "/weather/",
        json={
            "city": "New York",
            "temperature": 22.5,
            "description": "Sunny",
            "date": "2022-01-01",
        },
    )
    response = client.get("/weather/New York")
    assert response.status_code == 200
    data = response.json()

    assert data["city"] == "New York"
    assert data["temperature"] == 22.5
    assert data["description"] == "Sunny"
    assert data["date"] == "2022-01-01"


def test_get_weather_data_not_found():
    response = client.get("/weather/UnknownCity")
    assert response.status_code == 404
    assert response.json() == {"detail": "City not found"}
