"""Integration tests for the Genres endpoint."""

import pytest


@pytest.mark.asyncio
async def test_get_genres_returns_200(client):
    """Should return 200 and a list of genres."""
    response = await client.get("/api/genres")

    assert response.status_code == 200
    data = response.json()
    assert "genres" in data
    assert isinstance(data["genres"], list)


@pytest.mark.asyncio
async def test_get_genres_returns_known_genre(client):
    """Should include a known genre like 'samba' in the list."""
    response = await client.get("/api/genres")

    data = response.json()
    # Nosso banco tem 20 gêneros curados
    assert len(data["genres"]) >= 1
    genre_names = data["genres"]
    assert "samba" in genre_names


@pytest.mark.asyncio
async def test_get_invalid_endpoint_returns_404(client):
    """Should return 404 for non-existent API routes."""
    response = await client.get("/api/invalid-route")

    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Resource not found"


@pytest.mark.asyncio
async def test_get_genres_response_matches_schema(client):
    """Should validate response against GenreListResponse schema."""
    from app.schemas.api import GenreListResponse

    response = await client.get("/api/genres")
    data = response.json()

    GenreListResponse(**data)
    assert isinstance(data["genres"], list)
