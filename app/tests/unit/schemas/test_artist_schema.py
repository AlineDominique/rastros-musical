import pytest
from pydantic import ValidationError

from app.schemas.artist import ArtistSchema


@pytest.fixture
def valid_artist_payload() -> dict:
    """Provides a standardized valid artist payload for tests."""
    return {
        "name": "Sepultura",
        "origin_country": "Brazil",
        "latitude": -19.9167,
        "longitude": -43.9333,
        "genre": "Thrash Metal",
    }


def test_artist_schema_instantiation(valid_artist_payload):
    """Validate that a correctly formatted payload creates a valid ArtistSchema."""
    artist = ArtistSchema(**valid_artist_payload)
    assert artist.name == valid_artist_payload["name"]
    assert artist.latitude == valid_artist_payload["latitude"]


@pytest.mark.parametrize(
    "invalid_payload",
    [
        {
            "name": "",
            "origin_country": "Brazil",
            "latitude": 0,
            "longitude": 0,
        },  # Empty name
        {
            "name": "Band",
            "origin_country": "Brazil",
            "latitude": 91,
            "longitude": 0,
        },  # Lat high
        {
            "name": "Band",
            "origin_country": "Brazil",
            "latitude": 0,
            "longitude": 181,
        },  # Long high
        {
            "name": "Band",
            "origin_country": "Brazil",
            "latitude": "invalid",
            "longitude": 0,
        },  # Wrong type
    ],
)
def test_artist_schema_validation_fails(invalid_payload):
    """Ensures the schema strictly rejects malformed or out-of-bounds payloads.

    Each case in parametrization represents a complete, explicit failure
    scenario, ensuring no shared state between valid and invalid tests.
    """
    with pytest.raises(ValidationError):
        ArtistSchema(**invalid_payload)
