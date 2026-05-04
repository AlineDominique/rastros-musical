"""Main entry point for the FastAPI application and route definitions."""

import logging

from fastapi import FastAPI

from app.exceptions.handlers import internal_error_handler, not_found_handler
from app.middleware.logging import log_requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

app = FastAPI(
    title="Rastros Musical API",
    description="API for tracking music propagation between LatAm and Asia",
    version="0.1.0",
)

# Middlewares
app.middleware("http")(log_requests)

# Exception handlers
app.add_exception_handler(404, not_found_handler)
app.add_exception_handler(500, internal_error_handler)


@app.get("/", tags=["Health"], response_model=dict[str, str])
async def root() -> dict[str, str]:
    """Provides a basic health check and welcome message for the API.

    Returns:
        Dict[str, str]: A dictionary containing the API status,
            a welcome message, and the documentation link.
    """
    return {
        "message": "Rastros Musical API is running",
        "status": "online",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"], response_model=dict[str, str])
async def health_check() -> dict[str, str]:
    """Verifies the operational status of the application.

    Returns:
        Dict[str, str]: A simple dictionary indicating the health status.
    """
    return {"status": "healthy"}
