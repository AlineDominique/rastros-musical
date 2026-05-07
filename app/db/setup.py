"""Database setup — creates all schemas and tables."""

import duckdb

from app.db.bronze import create_bronze_tables
from app.db.database import db_manager
from app.db.seed_location import seed_location
from app.db.silver import create_silver_tables
from app.ingestion.gold_loader import GoldLoader
from app.ingestion.silver_loader import SilverLoader

_SCHEMAS = ("bronze", "silver", "gold")


def setup_all() -> None:
    """Run full database setup: schemas, tables, and country seed data."""
    with db_manager.get_connection() as conn:
        setup_database(conn)
        seed_location(conn)
        print("Database setup complete.")


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
    """Run complete ETL pipeline: Silver and Gold layers."""
    with db_manager.get_connection() as conn:
        conn.execute("DELETE FROM silver.artist_genre")
        conn.execute("DELETE FROM silver.artist")
        conn.execute("DELETE FROM silver.genre")

        print("Loading Silver...")
        silver = SilverLoader(conn)
        silver.load_artists()
        silver.load_genres()
        silver.load_artist_genres()

        artists = conn.execute("SELECT COUNT(*) FROM silver.artist").fetchone()[0]
        print(f"Silver artists: {artists}")

        print("Loading Gold...")
        gold = GoldLoader(conn)
        gold.load_genre_first_appearance()

        records = conn.execute(
            "SELECT COUNT(*) FROM gold.genre_first_appearance"
        ).fetchone()[0]
        print(f"Gold records: {records}")
