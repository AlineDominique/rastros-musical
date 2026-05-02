"""Unit and integration tests for the main API endpoints."""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_main():
    """Tests the root endpoint for correct status and message."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Rastros Musical API is running",
        "status": "online",
        "docs": "/docs",
    }
