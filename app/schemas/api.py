"""Response schemas for API endpoints."""

from pydantic import BaseModel, Field


class GenreListResponse(BaseModel):
    """Response schema for GET /api/genres."""

    genres: list[str] = Field(
        ..., description="List of genre names in alphabetical order"
    )


class CountryInfo(BaseModel):
    """Schema for a country in the propagation response."""

    country_code: str = Field(..., description="ISO 3166-1 alpha-2 country code")
    lat: float = Field(..., description="Latitude coordinate")
    lon: float = Field(..., description="Longitude coordinate")
    first_year: int = Field(..., description="Year of first appearance")
    source: str = Field(..., description="Data source: curated_origin or google_trends")


class PropagationResponse(BaseModel):
    """Response schema for GET /api/propagation."""

    genre: str = Field(..., description="Genre name")
    year: int = Field(..., description="Maximum year filter applied")
    countries: list[CountryInfo] = Field(
        ..., description="Countries where the genre appeared"
    )
