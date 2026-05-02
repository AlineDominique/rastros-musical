import pytest
from pydantic import ValidationError

from app.schemas.genre import GenreSchema


@pytest.fixture
def valid_genre_payload() -> dict:
    """Provides a standardized valid genre payload for tests."""
    return {
        "name": "Heavy Metal",
        "region_origin": "United Kingdom",
        "subgenres": ["Thrash Metal", "Death Metal"],
        "is_active": True,
    }


def test_genre_schema_success(valid_genre_payload):
    """Verifies that a valid genre payload is correctly instantiated."""
    genre = GenreSchema(**valid_genre_payload)
    assert genre.name == "Heavy Metal"
    assert "Thrash Metal" in genre.subgenres


@pytest.mark.parametrize(
    "invalid_payload",
    [
        {"name": "", "region_origin": "UK"},  # Empty name
        {
            "name": "Metal",
            "subgenres": "Thrash",
        },  # Subgenres should be a list, not a string
        {"name": "Metal", "is_active": "not-a-boolean"},  # Type mismatch
    ],
)
def test_genre_schema_validation_fails(invalid_payload):
    """Ensure the schema rejects invalid payloads.

    Validate that incorrect types or empty mandatory fields trigger a
    ValidationError.
    """
    with pytest.raises(ValidationError):
        GenreSchema(**invalid_payload)
