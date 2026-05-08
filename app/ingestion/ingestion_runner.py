"""Main ingestion runner — orchestrates multi-source data loading into Bronze."""

import logging

from app.db.database import db_manager
from app.ingestion.bronze_loader import BronzeLoader
from app.ingestion.genre_origins import GENRE_ORIGINS
from app.ingestion.genres import ALL_GENRES
from app.middleware.logging_config import setup_logging

setup_logging()
logger = logging.getLogger("rastros-musical.ingestion")


def _generate_genre_id(genre_name: str) -> str:
    """Generate a local genre ID from the genre name.

    Args:
        genre_name: Genre name (e.g., 'k-pop', 'samba').

    Returns:
        Local genre ID string.
    """
    return f"genre-{genre_name.replace(' ', '-').lower()}"


def run_ingestion() -> None:
    """Load genre origins into Bronze layer.

    Uses curated data from Wikipedia and musicological sources
    to populate the Bronze layer with validated genre origins.
    """
    stats = {"genres_processed": 0, "genres_failed": 0}

    logger.info("Starting ingestion for %d genres", len(ALL_GENRES))

    with db_manager.get_connection() as conn:
        loader = BronzeLoader(conn)

        for genre_name in ALL_GENRES:
            logger.info("Processing genre: %s", genre_name)

            try:
                origin = GENRE_ORIGINS.get(genre_name)
                if not origin:
                    logger.warning("No origin data for genre: %s", genre_name)
                    stats["genres_failed"] += 1
                    continue

                genre_id = _generate_genre_id(genre_name)
                loader.insert_genre({"genre_id": genre_id, "name": genre_name})

                # Insert origin as a virtual artist representing the genre's birthplace
                artist_id = f"origin-{genre_id}"
                loader.insert_artist(
                    {
                        "artist_id": artist_id,
                        "name": f"{genre_name} (Origin)",
                        "country_code": origin["country_code"],
                        "latitude": None,
                        "longitude": None,
                    }
                )
                loader.insert_artist_genre(
                    {
                        "artist_id": artist_id,
                        "genre_id": genre_id,
                        "start_date": str(origin["year_start"]),
                        "end_date": None,
                    }
                )

                stats["genres_processed"] += 1

            except Exception as e:
                logger.error("Failed to process genre %s: %s", genre_name, e)
                stats["genres_failed"] += 1

    logger.info(
        "Ingestion complete. Genres: %d processed, %d failed.",
        stats["genres_processed"],
        stats["genres_failed"],
    )
