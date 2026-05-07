"""Silver layer — transforms and loads cleaned data from Bronze."""

import logging

import duckdb

from app.middleware.logging_config import setup_logging

setup_logging()
logger = logging.getLogger("rastros-musical.silver")


def normalize_date(date_str: str | None) -> str | None:
    """Normalize a date string to YYYY-MM-DD format.

    Args:
        date_str: Raw date from MusicBrainz (e.g., '1988', '1988-03', '1988-03-15').

    Returns:
        Date in YYYY-MM-DD format, or None if input is None/empty.
    """
    if not date_str:
        return None
    if len(date_str) == 4:
        return f"{date_str}-01-01"
    if len(date_str) == 7:
        return f"{date_str}-01"
    return date_str


class SilverLoader:
    """Loads and transforms data from Bronze to Silver."""

    def __init__(self, conn: duckdb.DuckDBPyConnection) -> None:
        """Initialize with a DuckDB connection.

        Args:
            conn: Active DuckDB connection.
        """
        self.conn = conn

    def load_artists(self) -> None:
        """Load artists from bronze to silver with region and coordinates."""
        self.conn.execute("""
            INSERT INTO silver.artist (
                          artist_id, name, country_code,
                          latitude, longitude, region)
            SELECT
                b.artist_id,
                b.name,
                b.country_code,
                COALESCE(b.latitude, l.latitude),
                COALESCE(b.longitude, l.longitude),
                COALESCE(l.region, 'Other')
            FROM bronze.artist_raw b
            LEFT JOIN silver.location l ON b.country_code = l.country_code
            WHERE b.artist_id NOT IN (SELECT artist_id FROM silver.artist)
        """)
        count = self.conn.execute("SELECT COUNT(*) FROM silver.artist").fetchone()[0]
        logger.info("Artists loaded. Total in Silver: %d", count)

    def load_genres(self) -> None:
        """Load genres from bronze to silver."""
        self.conn.execute("""
            INSERT INTO silver.genre (genre_id, name, parent_genre_id)
            SELECT genre_id, name, parent_genre_id
            FROM bronze.genre_raw
            WHERE genre_id NOT IN (SELECT genre_id FROM silver.genre)
        """)
        count = self.conn.execute("SELECT COUNT(*) FROM silver.genre").fetchone()[0]
        logger.info("Genres loaded. Total in Silver: %d", count)

    def load_artist_genres(self) -> None:
        """Load artist-genre relations with normalized dates."""
        self.conn.execute("""
            INSERT INTO silver.artist_genre (artist_id, genre_id, start_date, end_date)
            SELECT
                b.artist_id,
                b.genre_id,
                CASE
                    WHEN LENGTH(b.start_date) = 4 THEN b.start_date || '-01-01'
                    WHEN LENGTH(b.start_date) = 7 THEN b.start_date || '-01'
                    ELSE b.start_date
                END,
                CASE
                    WHEN LENGTH(b.end_date) = 4 THEN b.end_date || '-01-01'
                    WHEN LENGTH(b.end_date) = 7 THEN b.end_date || '-01'
                    ELSE b.end_date
                END
            FROM bronze.artist_genre_raw b
            LEFT JOIN silver.artist_genre s
                ON b.artist_id = s.artist_id AND b.genre_id = s.genre_id
            WHERE s.artist_id IS NULL
        """)
        count = self.conn.execute(
            "SELECT COUNT(*) FROM silver.artist_genre"
        ).fetchone()[0]
        logger.info("Artist-genre relations loaded. Total in Silver: %d", count)
