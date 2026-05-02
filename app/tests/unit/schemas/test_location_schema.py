import pytest
from pydantic import ValidationError

from app.schemas.location import LocationSchema


@pytest.mark.parametrize(
    "country, code, expected_region",
    [
        ("Brazil", "BR", "Latam"),
        ("Japan", "JP", "Asia"),
        ("South Korea", "KR", "Asia"),
        ("Colombia", "CO", "Latam"),
        ("Russia", "RU", "Asia"),
        ("Uruguay", "UY", "Latam"),
        ("Uzbekistan", "UZ", "Asia"),
        ("Thailand", "TH", "Asia"),
        ("Guatemala", "GT", "Latam"),
    ],
)
def test_location_valid_regions(country, code, expected_region):
    """Validate that valid ISO codes assign the correct region."""
    data = {"country": country, "country_code": code, "latitude": 0.0, "longitude": 0.0}
    loc = LocationSchema(**data)
    assert loc.region == expected_region


@pytest.mark.parametrize("invalid_code", ["FR", "DE", "US", "ZA"])
def test_location_invalid_regions(invalid_code):
    """Ensure codes outside LatAm/Asia (like France or USA) raise ValidationError."""
    data = {
        "country": "Out of Scope",
        "country_code": invalid_code,
        "latitude": 0.0,
        "longitude": 0.0,
    }
    with pytest.raises(ValidationError, match="outside LatAm or Asia scope"):
        LocationSchema(**data)
