"""Global exception handlers for the FastAPI application."""

import logging

from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger("rastros-musical")


async def not_found_handler(request: Request, exc) -> JSONResponse:
    """Custom 404 response.

    Args:
        request: The incoming HTTP request.
        exc: The exception that was raised.

    Returns:
        JSONResponse with 404 status.
    """
    return JSONResponse(
        status_code=404,
        content={"detail": "Resource not found"},
    )


async def internal_error_handler(request: Request, exc) -> JSONResponse:
    """Custom 500 response with logging.

    Args:
        request: The incoming HTTP request.
        exc: The exception that was raised.

    Returns:
        JSONResponse with 500 status.
    """
    logger.error("Internal server error on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )
