"""Integration tests for the logging middleware."""

from unittest.mock import patch

import pytest


@pytest.mark.asyncio
async def test_log_requests_adds_request_id(client):
    """Should add X-Request-ID header to the response."""
    response = await client.get("/health")

    assert response.status_code == 200
    assert "X-Request-ID" in response.headers
    assert len(response.headers["X-Request-ID"]) == 8


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "path,expected_status,log_level",
    [
        ("/health", 200, "info"),
        ("/", 200, "info"),
        ("/nonexistent", 404, "warning"),
    ],
)
async def test_middleware_logs_real_output(client, path, expected_status, log_level):
    """Should log real output with correct level and message."""
    logger_attr = f"app.middleware.logging.logger.{log_level}"

    with patch(logger_attr) as mock_log:
        response = await client.get(path)

        assert response.status_code == expected_status
        mock_log.assert_called_once()

        format_string = mock_log.call_args[0][0]
        args = mock_log.call_args[0][1:]
        logged_message = format_string % args

        assert path in logged_message
        assert str(expected_status) in logged_message
