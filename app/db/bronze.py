"""Bronze layer — raw data tables."""

import duckdb

_TABLE_ARTIST_RAW = """
    CREATE TABLE IF NOT EXISTS bronze.artist_raw (
        artist_id INTEGER,
        name VARCHAR,
        country_code VARCHAR(2),
        latitude DOUBLE,
        longitude DOUBLE,
        ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
"""

_TABLE_GENRE_RAW = """
    CREATE TABLE IF NOT EXISTS bronze.genre_raw (
        genre_id INTEGER,
        name VARCHAR,
        parent_genre_id INTEGER,
        ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
"""

_TABLE_ARTIST_GENRE_RAW = """
    CREATE TABLE IF NOT EXISTS bronze.artist_genre_raw (
        artist_id INTEGER,
        genre_id INTEGER,
        start_date DATE,
        end_date DATE,
        ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
"""


def create_bronze_tables(conn: duckdb.DuckDBPyConnection) -> None:
    """Create raw ingestion tables in the bronze schema.

    Args:
        conn: DuckDB connection.
    """
    for sql in (_TABLE_ARTIST_RAW, _TABLE_GENRE_RAW, _TABLE_ARTIST_GENRE_RAW):
        conn.execute(sql)
