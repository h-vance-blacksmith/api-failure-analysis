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

def test_data_no_auth():
    response = client.get("/api/v1/data")
    assert response.status_code == 401

def test_resource_not_found():
    response = client.get("/api/v1/resource/999")
    assert response.status_code == 404
