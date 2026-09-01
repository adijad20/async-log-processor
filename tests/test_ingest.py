from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    """Verify that the health check endpoint returns 200 and healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "async-log-processor"
    }


def test_ingest_valid_log():
    """Verify valid payload receives 202 Accepted with expected schema response."""
    payload = {
        "client_id": "auth-service",
        "timestamp": "2026-09-01T12:00:00Z",
        "level": "INFO",
        "message": "User login successful",
        "metadata": {"user_id": 1042}
    }
    response = client.post("/v1/logs", json=payload)
    assert response.status_code == 202
    
    data = response.json()
    assert data["status"] == "accepted"
    assert data["client_id"] == "auth-service"
    assert "received_at" in data


def test_ingest_invalid_log_level():
    """Verify that invalid log levels trigger automated 422 validation error."""
    payload = {
        "client_id": "auth-service",
        "level": "CRITICAL_PANIC",  # Not in LogLevel Enum
        "message": "Something exploded"
    }
    response = client.post("/v1/logs", json=payload)
    assert response.status_code == 422


def test_ingest_short_client_id():
    """Verify client_id shorter than 3 characters is rejected."""
    payload = {
        "client_id": "ab",  # min_length is 3
        "level": "WARN",
        "message": "Short client ID check"
    }
    response = client.post("/v1/logs", json=payload)
    assert response.status_code == 422


def test_client_id_sanitization():
    """Verify that client_id whitespace is stripped and transformed to lowercase."""
    payload = {
        "client_id": "  PAYMENT-SERVICE  ",
        "level": "ERROR",
        "message": "Payment failed"
    }
    response = client.post("/v1/logs", json=payload)
    assert response.status_code == 202
    assert response.json()["client_id"] == "payment-service"