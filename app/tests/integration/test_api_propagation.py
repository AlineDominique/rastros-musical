"""Integration tests for the Propagation endpoint."""

import pytest


@pytest.mark.asyncio
async def test_get_propagation_returns_200(client):
    """Should return 200 and country list for a valid genre and year."""
    response = await client.get("/api/propagation?genre=samba&year=2000")

    assert response.status_code == 200
    data = response.json()
    assert "genre" in data
    assert data["genre"] == "samba"
    assert "year" in data
    assert "countries" in data
    assert isinstance(data["countries"], list)


@pytest.mark.asyncio
async def test_get_propagation_without_genre_returns_422(client):
    """Should return 422 when genre parameter is missing."""
    response = await client.get("/api/propagation")

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_propagation_invalid_genre_returns_404(client):
    """Should return 404 when invalid genre."""
    response = await client.get("/api/propagation?genre=fake-genre&year=2020")

    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "fake-genre" in data["detail"]


@pytest.mark.asyncio
async def test_get_propagation_response_matches_schema(client):
    """Should validate response against PropagationResponse schema."""
    from app.schemas.api import PropagationResponse

    response = await client.get("/api/propagation?genre=samba&year=2000")
    data = response.json()

    PropagationResponse(**data)
    assert data["genre"] == "samba"
    assert data["year"] == 2000
    assert isinstance(data["countries"], list)
