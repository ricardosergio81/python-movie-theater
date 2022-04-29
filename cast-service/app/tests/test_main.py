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


def test_post_cast(client: TestClient):
    response = client.post(
        "/api/v1/casts/",
        json={"name": "Ricardo Rosa", "nationality": "Brasil"},
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["name"] == "Ricardo Rosa"
    assert "id" in data
    cast_id = data["id"]

    response = client.get(f"/api/v1/casts/{cast_id}/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Ricardo Rosa"
    assert data["id"] == cast_id


def test_get_cast(client: TestClient):
    cast_id = 1
    response = client.get(f"/api/v1/casts/{cast_id}/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Ricardo Rosa"
    assert data["id"] == cast_id


def test_get_all_cast(client: TestClient):
    cast_id = 1
    response = client.get(f"/api/v1/casts/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["name"] == "Ricardo Rosa"
    assert data[0]["id"] == cast_id


def test_put_cast(client: TestClient):
    cast_id = 1
    response = client.put(
        f"/api/v1/casts/{cast_id}/",
        json={"name": "Name changed"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Name changed"
    assert "id" in data
    assert data["id"] == cast_id


def test_put_cast_id_not_found(client: TestClient):
    cast_id = 9999999
    response = client.put(
        f"/api/v1/casts/{cast_id}/",
        json={"name": "Name changed"}
    )
    assert response.status_code == 404, response.text


def test_get_cast_not_found(client: TestClient):
    cast_id = 9999999
    response = client.get(f"/api/v1/casts/{cast_id}/")
    assert response.status_code == 404, response.text
