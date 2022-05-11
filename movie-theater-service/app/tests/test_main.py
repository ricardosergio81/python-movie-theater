import pytest
from starlette.testclient import TestClient
from app.main import app
from fastapi import FastAPI
from typing import Generator
from ..api.database import Base, engine, SessionLocal


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield SessionLocal()


# Create a new application for testing
@pytest.fixture
def app() -> FastAPI:
    from app.main import app
    return app


@pytest.fixture()
def client(app: FastAPI):
    with TestClient(app) as client:  # context manager will invoke startup event
        yield client


def test_post_movie_theater(client: TestClient):
    response = client.post(
        "/api/v1/movies-theater/",
        json={"name": "Ricardo Rosa"},
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["name"] == "Ricardo Rosa"
    assert "id" in data
    movie_theater_id = data["id"]

    response = client.get(f"/api/v1/movies-theater/{movie_theater_id}/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Ricardo Rosa"
    assert data["id"] == movie_theater_id


def test_get_movie_theater(client: TestClient):
    movie_theater_id = 1
    response = client.get(f"/api/v1/movies-theater/{movie_theater_id}/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Ricardo Rosa"
    assert data["id"] == movie_theater_id


def test_get_all_movie_theater(client: TestClient):
    movie_theater_id = 1
    response = client.get(f"/api/v1/movies-theater/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["name"] == "Ricardo Rosa"
    assert data[0]["id"] == movie_theater_id


def test_put_movie_theater(client: TestClient):
    movie_theater_id = 1
    response = client.put(
        f"/api/v1/movies-theater/{movie_theater_id}/",
        json={"name": "Name changed"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Name changed"
    assert "id" in data
    assert data["id"] == movie_theater_id


def test_put_movie_theater_id_not_found(client: TestClient):
    movie_theater_id = 9999999
    response = client.put(
        f"/api/v1/movies-theater/{movie_theater_id}/",
        json={"name": "Name changed"}
    )
    assert response.status_code == 404, response.text


def test_get_movie_theater_not_found(client: TestClient):
    movie_theater_id = 9999999
    response = client.get(f"/api/v1/movies-theater/{movie_theater_id}/")
    assert response.status_code == 404, response.text
