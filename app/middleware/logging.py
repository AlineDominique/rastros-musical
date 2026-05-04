"""Structured logging middleware for request tracing."""

import logging
import time
import uuid

from fastapi import Request, Response

logger = logging.getLogger("rastros-musical")


def _log_request(
    level: int,
    request_id: str,
    method: str,
    path: str,
    status_code: int,
    duration: float,
) -> None:
    """Log a request at the given level.

    Args:
        level: Logging level (INFO, WARNING, ERROR).
        request_id: Unique request identifier.
        method: HTTP method.
        path: Request path.
        status_code: HTTP response status code.
        duration: Request duration in seconds.
    """
    log_methods = {
        logging.ERROR: logger.error,
        logging.WARNING: logger.warning,
        logging.INFO: logger.info,
    }

    log = log_methods.get(level, logger.info)
    log(
        "[%s] %s %s -> %s (%.3fs)",
        request_id,
        method,
        path,
        status_code,
        duration,
    )


async def log_requests(request: Request, call_next):
    """Log all requests with method, path, status and duration.

    Log level varies by status code:
        - 2xx/3xx: INFO
        - 4xx: WARNING
        - 5xx: ERROR

    Args:
        request: The incoming HTTP request.
        call_next: The next middleware or route handler.

    Returns:
        The HTTP response with X-Request-ID header added.
    """
    request_id = str(uuid.uuid4())[:8]
    start_time = time.time()

    response: Response = await call_next(request)

    duration = time.time() - start_time

    if response.status_code >= 500:
        level = logging.ERROR
    elif response.status_code >= 400:
        level = logging.WARNING
    else:
        level = logging.INFO

    _log_request(
        level,
        request_id,
        request.method,
        request.url.path,
        response.status_code,
        duration,
    )

    response.headers["X-Request-ID"] = request_id
    return response
