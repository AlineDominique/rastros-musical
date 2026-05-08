"""Gold layer — analytical tables for the MVP."""

import logging

import duckdb

from app.middleware.logging_config import setup_logging

setup_logging()
logger = logging.getLogger("rastros-musical.gold")


class GoldLoader:
    """Creates analytical tables in the Gold layer."""

    def __init__(self, conn: duckdb.DuckDBPyConnection) -> None:
        """Initialize with a DuckDB connection.

        Args:
            conn: Active DuckDB connection.
        """
        self.conn = conn

    def load_genre_first_appearance(self) -> None:
        """Create and populate the hero table with curated genre origins."""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS gold.genre_first_appearance (
                genre VARCHAR NOT NULL,
                target_country VARCHAR(2) NOT NULL,
                target_lat DOUBLE,
                target_lon DOUBLE,
                first_year INTEGER,
                source VARCHAR,
                PRIMARY KEY (genre, target_country)
            )
        """)

        self.conn.execute("""
            INSERT OR REPLACE INTO gold.genre_first_appearance
                (genre, target_country, target_lat, target_lon, first_year, source)
            SELECT
                g.name AS genre,
                a.country_code AS target_country,
                l.latitude AS target_lat,
                l.longitude AS target_lon,
                CAST(EXTRACT(YEAR FROM MIN(ag.start_date)) AS INTEGER) AS first_year,
                'curated_origin' AS source
            FROM silver.artist_genre ag
            JOIN silver.artist a ON ag.artist_id = a.artist_id
            JOIN silver.genre g ON ag.genre_id = g.genre_id
            LEFT JOIN silver.location l ON a.country_code = l.country_code
            WHERE a.country_code IS NOT NULL
                AND a.country_code != ''
                AND ag.start_date IS NOT NULL
            GROUP BY g.name, a.country_code, l.latitude, l.longitude
        """)

        count = self.conn.execute(
            "SELECT COUNT(*) FROM gold.genre_first_appearance"
        ).fetchone()[0]
        logger.info("Genre origins loaded: %d records", count)

    def load_genre_propagation(self) -> None:
        """Load Google Trends propagation data into Gold."""
        self.conn.execute("""
            INSERT OR REPLACE INTO gold.genre_first_appearance
                (genre, target_country, target_lat, target_lon, first_year, source)
            SELECT
                gp.genre,
                gp.country_code AS target_country,
                l.latitude AS target_lat,
                l.longitude AS target_lon,
                gp.first_year,
                'google_trends' AS source
            FROM silver.genre_propagation gp
            LEFT JOIN silver.location l ON gp.country_code = l.country_code
            WHERE gp.first_year IS NOT NULL
        """)

        count = self.conn.execute(
            "SELECT COUNT(*) FROM gold.genre_first_appearance "
            "WHERE source = 'google_trends'"
        ).fetchone()[0]
        logger.info("Propagation records loaded: %d", count)
