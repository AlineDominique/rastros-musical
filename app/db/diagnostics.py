"""Database diagnostic commands (read-only)."""

import logging
import os
import sys

from app.db.database import db_manager
from app.middleware.logging_config import setup_logging

setup_logging()
logger = logging.getLogger("rastros-musical.diagnostics")


def show_stats():
    """Show database overview."""
    with db_manager.get_connection() as conn:
        bronze_artists = conn.execute(
            "SELECT COUNT(*) FROM bronze.artist_raw"
        ).fetchone()[0]
        bronze_genres = conn.execute(
            "SELECT COUNT(*) FROM bronze.genre_raw"
        ).fetchone()[0]
        bronze_relations = conn.execute(
            "SELECT COUNT(*) FROM bronze.artist_genre_raw"
        ).fetchone()[0]
        silver_artists = conn.execute("SELECT COUNT(*) FROM silver.artist").fetchone()[
            0
        ]
        silver_genres = conn.execute("SELECT COUNT(*) FROM silver.genre").fetchone()[0]
        silver_relations = conn.execute(
            "SELECT COUNT(*) FROM silver.artist_genre"
        ).fetchone()[0]
        locations = conn.execute("SELECT COUNT(*) FROM silver.location").fetchone()[0]
        gold_records = conn.execute(
            "SELECT COUNT(*) FROM gold.genre_first_appearance"
        ).fetchone()[0]
        size = os.path.getsize(db_manager.db_path)

        logger.info("=== Bronze ===")
        logger.info("  Artists:   %d", bronze_artists)
        logger.info("  Genres:    %d", bronze_genres)
        logger.info("  Relations: %d", bronze_relations)
        logger.info("=== Silver ===")
        logger.info("  Artists:   %d", silver_artists)
        logger.info("  Genres:    %d", silver_genres)
        logger.info("  Relations: %d", silver_relations)
        logger.info("  Locations: %d", locations)
        logger.info("=== Gold ===")
        logger.info("  Records:   %d", gold_records)
        logger.info("=== Database ===")
        logger.info("  Size:      %.1f KB", size / 1024)


def show_top_countries():
    """Show top 10 countries by artist count."""
    with db_manager.get_connection() as conn:
        logger.info("Top 10 countries by artist count:")
        for row in conn.execute(
            "SELECT country_code, COUNT(*) as c FROM bronze.artist_raw "
            "WHERE country_code != '' GROUP BY country_code ORDER BY c DESC LIMIT 10"
        ).fetchall():
            logger.info("  %s: %d", row[0], row[1])


def show_top_genres():
    """Show genres by artist count."""
    with db_manager.get_connection() as conn:
        logger.info("Genres by artist count:")
        for row in conn.execute(
            "SELECT g.name, COUNT(agr.artist_id) as c "
            "FROM bronze.genre_raw g "
            "JOIN bronze.artist_genre_raw agr ON g.genre_id = agr.genre_id "
            "GROUP BY g.name ORDER BY c DESC"
        ).fetchall():
            logger.info("  %s: %d", row[0], row[1])


def show_sample():
    """Show 10 sample artists."""
    with db_manager.get_connection() as conn:
        logger.info("Sample artists:")
        for row in conn.execute(
            "SELECT name, country_code FROM bronze.artist_raw "
            "WHERE country_code != '' LIMIT 10"
        ).fetchall():
            logger.info("  %s (%s)", row[0], row[1])


def show_gold_sample():
    """Show sample from gold layer."""
    with db_manager.get_connection() as conn:
        logger.info("Sample from Gold (genre_first_appearance):")
        for row in conn.execute(
            "SELECT * FROM gold.genre_first_appearance "
            "ORDER BY genre, first_year LIMIT 15"
        ).fetchall():
            logger.info("  %s -> %s (%d)", row[0], row[1], row[4])


if __name__ == "__main__":
    commands = {
        "stats": show_stats,
        "countries": show_top_countries,
        "genres": show_top_genres,
        "sample": show_sample,
        "gold": show_gold_sample,
    }
    cmd = sys.argv[1] if len(sys.argv) > 1 else "stats"
    commands.get(cmd, show_stats)()
