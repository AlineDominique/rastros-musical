"""Tests for exception handlers."""

import json
from unittest.mock import MagicMock

import pytest

from app.exceptions.handlers import internal_error_handler


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "path,expected_status,expected_detail",
    [
        ("/nonexistent", 404, "Resource not found"),
        ("/invalid-endpoint", 404, "Resource not found"),
    ],
)
async def test_404_returns_json(client, path, expected_status, expected_detail):
    """Should return JSON with detail message for 404 on unknown routes."""
    response = await client.get(path)

    assert response.status_code == expected_status
    assert response.json() == {"detail": expected_detail}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "path,expected_status,expected_body",
    [
        ("/health", 200, {"status": "healthy"}),
        (
            "/",
            200,
            {
                "message": "Rastros Musical API is running",
                "status": "online",
                "docs": "/docs",
            },
        ),
    ],
)
async def test_successful_endpoints(client, path, expected_status, expected_body):
    """Should return correct status and body for valid endpoints."""
    response = await client.get(path)
    assert response.status_code == expected_status
    assert response.json() == expected_body


@pytest.mark.asyncio
async def test_internal_error_handler_returns_json():
    """Should return JSON with detail message for 500."""
    request = MagicMock()
    request.method = "GET"
    request.url.path = "/some-endpoint"
    exc = RuntimeError("Simulated error")

    response = await internal_error_handler(request, exc)

    assert response.status_code == 500
    assert json.loads(response.body) == {"detail": "Internal server error"}
