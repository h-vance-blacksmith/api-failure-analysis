from fastapi.testclient import TestClient

from app.api import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_login_invalid():
    response = client.post("/login", json={"username": "admin", "password": "wrong"})
    assert response.status_code == 401


def test_login_valid():
    response = client.post(
        "/login",
        json={"username": "admin", "password": "password123"},
    )
    assert response.status_code == 200
    assert response.json() == {"token": "valid-token-xyz"}


def test_data_no_auth():
    response = client.get("/api/v1/data")
    assert response.status_code == 401


def test_data_valid_auth():
    response = client.get(
        "/api/v1/data",
        headers={"Authorization": "Bearer valid-token-xyz"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "data": "Secret research results",
        "access": "admin",
    }


def test_resource_not_found():
    response = client.get("/api/v1/resource/999")
    assert response.status_code == 404


def test_trigger_error_returns_500():
    error_client = TestClient(app, raise_server_exceptions=False)
    response = error_client.get("/api/v1/trigger-error")
    assert response.status_code == 500
