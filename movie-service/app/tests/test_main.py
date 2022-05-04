import pytest
import os
from starlette.testclient import TestClient
from app.main import app
from requests_mock.mocker import Mocker
from fastapi import FastAPI
from typing import Generator
from ..api.database import Base, engine, SessionLocal
from app.api.service import is_cast_present


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


def test_cast_service(requests_mock: Mocker):
    cast_id = "1"
    url = os.environ.get('CAST_SERVICE_HOST_URL') + cast_id
    requests_mock.get(url, text='data', status_code=200)

    assert is_cast_present(cast_id) == True


def test_post_movie(client: TestClient, requests_mock: Mocker):
    cast_id = "1"
    url = os.environ.get('CAST_SERVICE_HOST_URL') + cast_id
    requests_mock.get(url, text='data', status_code=200)

    requests_mock.real_http = True
    response = client.post(
        "/api/v1/movies/",
        json={"name": "Homem Aranha",
              "plot": "Homem picado por uma aranha",
              "genres": ["Ação", "Romance"],
              "casts_id": [cast_id],
              "year": 2020
              }
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["name"] == "Homem Aranha"
    assert "id" in data
    movie_id = data["id"]

    response = client.get(f"/api/v1/movies/{movie_id}/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Homem Aranha"
    assert data["id"] == movie_id


def test_post_movie_cast_not_found(client: TestClient, requests_mock: Mocker):
    cast_id = "1"
    url = os.environ.get('CAST_SERVICE_HOST_URL') + cast_id
    requests_mock.get(url, text='data', status_code=404)

    requests_mock.real_http = True
    response = client.post(
        "/api/v1/movies/",
        json={"name": "Homem Aranha",
              "plot": "Homem picado por uma aranha",
              "genres": ["Ação", "Romance"],
              "casts_id": [cast_id],
              "year": 2020
              }
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Cast with given id:1 not found"


def test_get_movie(client: TestClient):
    movie_id = 1
    response = client.get(f"/api/v1/movies/{movie_id}/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Homem Aranha"
    assert data["id"] == movie_id


def test_get_all_movie(client: TestClient):
    movie_id = 1
    response = client.get(f"/api/v1/movies/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["name"] == "Homem Aranha"
    assert data[0]["id"] == movie_id


def test_put_movie(client: TestClient):
    movie_id = 1
    response = client.put(
        f"/api/v1/movies/{movie_id}/",
        json={"name": "Spider Man: first",
              "genres": ["Ação"]}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Spider Man: first"
    assert "id" in data
    assert data["id"] == movie_id


def test_put_movie_change_cast(client: TestClient, requests_mock: Mocker):
    cast_id = 2
    url = os.environ.get('CAST_SERVICE_HOST_URL') + str(cast_id)
    requests_mock.get(url, text='data', status_code=200)
    requests_mock.real_http = True
    movie_id = 1
    response = client.put(
        f"/api/v1/movies/{movie_id}/",
        json={"name": "Spider Man: first",
              "genres": ["Ação"],
              "casts_id": [cast_id],
              }
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Spider Man: first"
    assert "id" in data
    assert data["id"] == movie_id
    assert "casts_id" in data
    assert list(data["casts_id"])[0] == cast_id


def test_put_movie_change_cast_not_found(client: TestClient, requests_mock: Mocker):
    cast_id = 2
    url = os.environ.get('CAST_SERVICE_HOST_URL') + str(cast_id)
    requests_mock.get(url, text='data', status_code=404)
    requests_mock.real_http = True
    movie_id = 1
    response = client.put(
        f"/api/v1/movies/{movie_id}/",
        json={"name": "Spider Man: first",
              "genres": ["Ação"],
              "casts_id": [cast_id],
              }
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Cast with given id:2 not found"


def test_put_movie_id_not_found(client: TestClient):
    movie_id = 9999999
    response = client.put(
        f"/api/v1/movies/{movie_id}/",
        json={"name": "Homem Aranha"}
    )
    assert response.status_code == 404, response.text


def test_get_movie_not_found(client: TestClient):
    movie_id = 9999999
    response = client.get(f"/api/v1/movies/{movie_id}/")
    assert response.status_code == 404, response.text
