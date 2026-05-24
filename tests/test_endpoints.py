from fastapi.testclient import TestClient

import sys
sys.path.insert(0, "app")
from api import app, webhook_inbox

client = TestClient(app)


def setup_module():
    webhook_inbox.clear()


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_headers_endpoint():
    response = client.get("/d/headers")
    assert response.status_code == 200
    data = response.json()
    assert "headers" in data
    assert "request_id" in data
    assert "trace_id" in data


def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "counters_by_status" in data
    assert "total_requests" in data


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


def test_data_invalid_token():
    response = client.get(
        "/api/v1/data",
        headers={"Authorization": "Bearer invalid-token"},
    )
    assert response.status_code == 403


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


def test_resource_found():
    response = client.get("/api/v1/resource/50")
    assert response.status_code == 200


def test_trigger_error_returns_500():
    error_client = TestClient(app, raise_server_exceptions=False)
    response = error_client.get("/api/v1/trigger-error")
    assert response.status_code == 500


def test_list_incidents():
    response = client.get("/incidents")
    assert response.status_code == 200
    data = response.json()
    assert "incidents" in data
    assert len(data["incidents"]) > 0


def test_get_incident():
    response = client.get("/incidents/INC-001-auth-cascade")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "INC-001-auth-cascade"
    assert "timeline" in data
    assert "log_lines" in data
    assert "request_samples" in data


def test_get_incident_not_found():
    response = client.get("/incidents/INC-999")
    assert response.status_code == 404


def test_evidence_bundle():
    response = client.get("/incidents/INC-001-auth-cascade/evidence-bundle")
    assert response.status_code == 200
    data = response.json()
    assert data["incident_id"] == "INC-001-auth-cascade"
    assert "timeline" in data
    assert "log_lines" in data
    assert "request_samples" in data
    assert "related_endpoints" in data
    assert "summary" in data


def test_replay_incident():
    response = client.post("/incidents/INC-001-auth-cascade/replay")
    assert response.status_code == 200
    data = response.json()
    assert data["incident_id"] == "INC-001-auth-cascade"
    assert "steps" in data
    assert "trace_id" in data


def test_webhook_inbound_valid():
    response = client.post(
        "/webhooks/inbound",
        json={"event": "order.shipped", "order_id": "ORD-123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "accepted"
    assert data["valid"]


def test_webhook_inbox():
    response = client.get("/webhooks/inbox")
    assert response.status_code == 200
    data = response.json()
    assert "deliveries" in data
    assert len(data["deliveries"]) > 0


def test_x_request_id_propagated():
    response = client.get(
        "/health",
        headers={"X-Request-ID": "test-req-001", "X-Trace-ID": "test-tx-001"},
    )
    assert response.headers.get("X-Request-ID") == "test-req-001"
    assert response.headers.get("X-Trace-ID") == "test-tx-001"
