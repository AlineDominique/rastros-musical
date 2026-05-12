"""Propagation endpoint."""

from fastapi import APIRouter, HTTPException, Query

from app.db.database import db_manager
from app.schemas.api import PropagationResponse

router = APIRouter(prefix="/api", tags=["Propagation"])

propagation_examples = {
    200: {
        "description": "Propagação do gênero nos países",
        "content": {
            "application/json": {
                "example": {
                    "genre": "tango",
                    "year": 2026,
                    "countries": [
                        {
                            "country_code": "AR",
                            "lat": -34.0,
                            "lon": -64.0,
                            "first_year": 1880,
                            "source": "curated_origin",
                        },
                        {
                            "country_code": "JP",
                            "lat": 36.0,
                            "lon": 138.0,
                            "first_year": 2004,
                            "source": "google_trends",
                        },
                        {
                            "country_code": "KR",
                            "lat": 37.0,
                            "lon": 127.5,
                            "first_year": 2004,
                            "source": "google_trends",
                        },
                    ],
                }
            }
        },
    },
    404: {
        "description": "Gênero não encontrado",
        "content": {
            "application/json": {"example": {"detail": "Genre 'funk' not found"}}
        },
    },
}


@router.get(
    "/propagation", response_model=PropagationResponse, responses=propagation_examples
)
async def get_propagation(
    genre: str = Query(..., description="Genre name (e.g., 'tango', 'k-pop')"),
    year: int = Query(2026, description="Maximum year to filter", ge=1200, le=2026),
) -> dict:
    """Return countries where the genre appeared up to the given year.

    Args:
        genre: Genre name.
        year: Maximum year filter.

    Returns:
        Dict with genre, year, and list of countries.

    Raises:
        HTTPException: 404 if genre is not found in the database.
    """
    with db_manager.get_connection() as conn:
        exists = conn.execute(
            "SELECT 1 FROM gold.genre_first_appearance WHERE genre = ?", [genre]
        ).fetchone()

        if not exists:
            raise HTTPException(status_code=404, detail=f"Genre '{genre}' not found")

        countries = conn.execute(
            """
            SELECT target_country, target_lat, target_lon, first_year, source
            FROM gold.genre_first_appearance
            WHERE genre = ? AND first_year <= ?
            ORDER BY first_year
            """,
            [genre, year],
        ).fetchall()

    return {
        "genre": genre,
        "year": year,
        "countries": [
            {
                "country_code": c[0],
                "lat": c[1],
                "lon": c[2],
                "first_year": c[3],
                "source": c[4],
            }
            for c in countries
        ],
    }
