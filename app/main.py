"""Main entry point for the FastAPI application and route definitions."""

from fastapi import FastAPI

app = FastAPI(
    title="Rastros Musical API",
    description="API for tracking music propagation between LatAm and Asia",
    version="0.1.0",
)


@app.get("/")
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


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Verifies the operational status of the application.

    Returns:
        Dict[str, str]: A simple dictionary indicating the health status.
    """
    return {"status": "healthy"}
