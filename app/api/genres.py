"""Genre listing endpoint."""

from fastapi import APIRouter

from app.db.database import db_manager
from app.schemas.api import GenreListResponse

router = APIRouter(prefix="/api", tags=["Genres"])

genres_examples = {
    200: {
        "description": "Lista de gêneros disponíveis",
        "content": {
            "application/json": {
                "example": {
                    "genres": [
                        "bachata",
                        "bollywood",
                        "bossa nova",
                        "cantopop",
                        "cumbia",
                        "dangdut",
                        "enka",
                        "j-pop",
                        "k-pop",
                        "mandopop",
                        "mariachi",
                        "merengue",
                        "mpb",
                        "qawwali",
                        "reggaeton",
                        "salsa",
                        "samba",
                        "sertanejo",
                        "tango",
                        "vallenato",
                    ]
                }
            }
        },
    },
    404: {
        "description": "Rota não encontrada",
        "content": {"application/json": {"example": {"detail": "Resource not found"}}},
    },
}


@router.get("/genres", response_model=GenreListResponse, responses=genres_examples)
async def get_genres() -> dict:
    """Return the list of unique genres available.

    Returns:
        Dict with a list of genre names ordered alphabetically.
    """
    with db_manager.get_connection() as conn:
        genres = conn.execute(
            "SELECT DISTINCT genre FROM gold.genre_first_appearance ORDER BY genre"
        ).fetchall()

    return {"genres": [g[0] for g in genres]}
