"""Database setup — creates all schemas and tables."""

import logging

import duckdb

from app.db.bronze import create_bronze_tables
from app.db.database import db_manager
from app.db.seed_location import seed_location
from app.db.silver import create_silver_tables
from app.ingestion.gold_loader import GoldLoader
from app.ingestion.silver_loader import SilverLoader
from app.middleware.logging_config import setup_logging

setup_logging()
logger = logging.getLogger("rastros-musical.setup")

_SCHEMAS = ("bronze", "silver", "gold")


def setup_all() -> None:
    """Run full database setup: schemas, tables, and country seed data."""
    with db_manager.get_connection() as conn:
        setup_database(conn)
        seed_location(conn)
        logger.info("Database setup complete.")


def setup_database(conn: duckdb.DuckDBPyConnection = None) -> None:
    """Initialize the database with all schemas and tables.

    Args:
        conn: DuckDB connection. If None, uses the default db_manager.
              The caller is responsible for closing if provided externally.
    """
    if conn is None:
        with db_manager.get_connection() as conn:
            _create_schemas(conn)
            _create_tables(conn)
    else:
        _create_schemas(conn)
        _create_tables(conn)


def _create_schemas(conn: duckdb.DuckDBPyConnection) -> None:
    """Create Medallion schemas."""
    for schema in _SCHEMAS:
        conn.execute(f"CREATE SCHEMA IF NOT EXISTS {schema};")


def _create_tables(conn: duckdb.DuckDBPyConnection) -> None:
    """Create all tables across layers."""
    create_bronze_tables(conn)
    create_silver_tables(conn)


def load_all() -> None:
    """Run complete ETL pipeline: Silver and Gold layers.

    Loads curated genre origins from Bronze into Silver, fetches
    Google Trends propagation data for all genre-country pairs,
    and generates the Gold layer with consolidated first appearances.
    """
    with db_manager.get_connection() as conn:
        logger.info("Clearing Silver and Gold layers...")
        conn.execute("DELETE FROM silver.artist_genre")
        conn.execute("DELETE FROM silver.artist")
        conn.execute("DELETE FROM silver.genre")
        conn.execute("DELETE FROM silver.genre_propagation")

        logger.info("Loading Silver...")
        silver = SilverLoader(conn)
        silver.load_artists()
        silver.load_genres()
        silver.load_artist_genres()

        countries = conn.execute("SELECT country_code FROM silver.location").fetchall()
        country_codes = [c[0] for c in countries]
        silver.load_genre_propagation(country_codes)

        logger.info("Loading Gold...")
        gold = GoldLoader(conn)
        gold.load_genre_first_appearance()
        gold.load_genre_propagation()

        records = conn.execute(
            "SELECT COUNT(*) FROM gold.genre_first_appearance"
        ).fetchone()[0]
        logger.info("Gold records: %d", records)
