"""Main ingestion runner — orchestrates MusicBrainz fetch and Bronze loading."""

import logging

from app.middleware.logging_config import setup_logging
from app.db.database import db_manager
from app.ingestion.musicbrainz import MusicBrainzClient
from app.ingestion.bronze_loader import BronzeLoader
from app.ingestion.genres import ALL_GENRES

setup_logging()
logger = logging.getLogger("rastros-musical.ingestion")


def _parse_artist(artist: dict) -> dict:
    """Extract relevant fields from a MusicBrainz artist.

    Args:
        artist: Raw artist dict from MusicBrainz API.

    Returns:
        Simplified artist dict ready for Bronze insertion.
    """
    return {
        "artist_id": artist.get("id"),
        "name": artist.get("name"),
        "country_code": artist.get("country", ""),
        "latitude": None,
        "longitude": None,
    }

def _generate_genre_id(genre_name: str) -> str:
    """Generate a local genre ID from the genre name.

    Args:
        genre_name: Genre name (e.g., 'k-pop', 'samba').

    Returns:
        Local genre ID string.
    """
    return f"genre-{genre_name.replace(' ', '-').lower()}"

def run_ingestion() -> None:
    """Fetch artists by genre from MusicBrainz and load into Bronze."""
    client = MusicBrainzClient()
    stats = {"genres_processed": 0, "genres_failed": 0, "artists_inserted": 0}

    logger.info("Starting ingestion for %d genres", len(ALL_GENRES))

    with db_manager.get_connection() as conn:
        loader = BronzeLoader(conn)

        for genre_name in ALL_GENRES:
            logger.info("Processing genre: %s", genre_name)

            try:
                genre_id = _generate_genre_id(genre_name)

                loader.insert_genre({"genre_id": genre_id, "name": genre_name})

                data = client.search_artists_by_genre(genre_name)
                artist_count = data.get("count", 0)
                logger.info("Found %d artists for genre: %s", artist_count, genre_name)

                for artist in data.get("artists", []):
                    try:
                        artist_data = _parse_artist(artist)
                        loader.insert_artist(artist_data)
                        loader.insert_artist_genre({
                            "artist_id": artist_data["artist_id"],
                            "genre_id": genre_id,
                            "start_date": artist.get("life-span", {}).get("begin"),
                            "end_date": artist.get("life-span", {}).get("end"),
                        })
                        stats["artists_inserted"] += 1
                    except Exception as e:
                        logger.error(
                            "Failed to insert artist %s: %s",
                            artist.get("name", "unknown"),
                            e,
                        )

                stats["genres_processed"] += 1

            except Exception as e:
                logger.error("Failed to process genre %s: %s", genre_name, e)
                stats["genres_failed"] += 1

    logger.info(
        "Ingestion complete. Genres: %d processed, %d failed. Artists inserted: %d",
        stats["genres_processed"],
        stats["genres_failed"],
        stats["artists_inserted"],
    )
