"""Tests for the logging middleware."""

import logging
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.middleware.logging import log_requests


@pytest.mark.asyncio
async def test_log_requests_adds_request_id(client):
    """Should add X-Request-ID header to the response."""
    response = await client.get("/health")

    assert response.status_code == 200
    assert "X-Request-ID" in response.headers
    assert len(response.headers["X-Request-ID"]) == 8


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "level,expected_method",
    [
        (logging.INFO, "info"),
        (logging.WARNING, "warning"),
        (logging.ERROR, "error"),
    ],
)
async def test_log_request_uses_correct_level(level, expected_method):
    """Should call the correct logger method based on level."""
    logger_attr = f"app.middleware.logging.logger.{expected_method}"

    with patch(logger_attr) as mock_log:
        from app.middleware.logging import _log_request

        _log_request(level, "abc123", "GET", "/test", 200, 0.005)

        mock_log.assert_called_once()
        args = mock_log.call_args[0]

        assert args[0] == "[%s] %s %s -> %s (%.3fs)"
        assert args[1] == "abc123"
        assert args[2] == "GET"
        assert args[3] == "/test"
        assert args[4] == 200
        assert args[5] == 0.005


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "method,path,expected_status",
    [
        ("GET", "/health", 200),
        ("GET", "/", 200),
    ],
)
async def test_log_info_on_success(client, method, path, expected_status):
    """Should log with INFO level for 2xx responses."""
    with patch("app.middleware.logging._log_request") as mock_log:
        response = await client.request(method, path)

        assert response.status_code == expected_status
        mock_log.assert_called_once()

        args = mock_log.call_args[0]
        assert args[0] == logging.INFO
        assert args[2] == method
        assert args[3] == path
        assert args[4] == expected_status


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "path",
    [
        "/nonexistent",
        "/invalid",
    ],
)
async def test_log_warning_on_client_error(client, path):
    """Should log with WARNING level for 4xx responses."""
    with patch("app.middleware.logging._log_request") as mock_log:
        response = await client.get(path)

        assert response.status_code == 404
        mock_log.assert_called_once()

        args = mock_log.call_args[0]
        assert args[0] == logging.WARNING
        assert args[2] == "GET"
        assert args[3] == path
        assert args[4] == 404


@pytest.mark.asyncio
async def test_middleware_dispatches_error_on_500():
    """Should dispatch ERROR level for 5xx responses."""
    request = MagicMock()
    request.method = "GET"
    request.url.path = "/test"

    response = MagicMock()
    response.status_code = 500

    call_next = AsyncMock(return_value=response)

    with patch("app.middleware.logging._log_request") as mock_log:
        await log_requests(request, call_next)

        mock_log.assert_called_once()
        assert mock_log.call_args[0][0] == logging.ERROR
        assert mock_log.call_args[0][3] == "/test"
        assert mock_log.call_args[0][4] == 500
