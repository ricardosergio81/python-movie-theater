from starlette.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_post_cast():
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


def test_put_cast():
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

def test_put_cast_id_not_found():
    cast_id = 9999999
    response = client.put(
        f"/api/v1/casts/{cast_id}/",
        json={"name": "Name changed"}
    )
    assert response.status_code == 404, response.text


def test_get_cast():
    cast_id = 1
    response = client.get(f"/api/v1/casts/{cast_id}/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Name changed"
    assert data["id"] == cast_id

def test_get_cast_not_found():
    cast_id = 9999999
    response = client.get(f"/api/v1/casts/{cast_id}/")
    assert response.status_code == 404, response.text
