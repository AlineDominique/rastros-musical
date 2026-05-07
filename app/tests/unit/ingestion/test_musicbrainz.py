"""Tests for MusicBrainz API client."""

from unittest.mock import patch

import pytest

from app.ingestion.musicbrainz import MusicBrainzClient


@pytest.fixture
def client():
    """MusicBrainz client with test user-agent."""
    return MusicBrainzClient(user_agent="RastrosMusical-Test/0.1")


def test_client_has_correct_base_url(client):
    """Should use MusicBrainz API base URL."""
    assert client.base_url == "https://musicbrainz.org/ws/2"


def test_client_has_user_agent(client):
    """Should have the provided user agent."""
    assert client.user_agent == "RastrosMusical-Test/0.1"


def test_search_artists_by_genre_returns_results(client):
    """Should return artists for a given genre."""
    mock_response = {
        "artists": [
            {
                "id": "artist-1",
                "name": "Chico Buarque",
                "country": "BR",
                "area": {"name": "Brazil"},
            }
        ],
        "count": 1,
    }

    with patch.object(client._client, "get") as mock_get:
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.raise_for_status = lambda: None

        result = client.search_artists_by_genre("Samba")

        assert result == mock_response
        mock_get.assert_called_once_with(
            "/artist",
            params={"query": 'tag:"Samba"', "limit": 100, "offset": 0, "fmt": "json"},
        )
