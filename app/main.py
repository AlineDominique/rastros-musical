"""Main entry point for the FastAPI application and route definitions."""

from fastapi import FastAPI

from app.api.genres import router as genres_router
from app.api.propagation import router as propagation_router
from app.exceptions.handlers import internal_error_handler, not_found_handler
from app.middleware.logging import log_requests
from app.middleware.logging_config import setup_logging

setup_logging()


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
app.include_router(genres_router)
app.include_router(propagation_router)


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
