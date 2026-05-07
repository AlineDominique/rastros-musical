"""Silver layer — cleaned and validated data."""

import duckdb

_TABLE_ARTIST = """
    CREATE TABLE IF NOT EXISTS silver.artist (
        artist_id VARCHAR PRIMARY KEY,
        name VARCHAR NOT NULL,
        country_code VARCHAR(2),
        latitude DOUBLE,
        longitude DOUBLE,
        region VARCHAR(5) CHECK (region IN ('Latam', 'Asia', 'Other')),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
"""

_TABLE_GENRE = """
    CREATE TABLE IF NOT EXISTS silver.genre (
        genre_id VARCHAR PRIMARY KEY,
        name VARCHAR NOT NULL,
        parent_genre_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
"""

_TABLE_ARTIST_GENRE = """
    CREATE TABLE IF NOT EXISTS silver.artist_genre (
        artist_id VARCHAR,
        genre_id VARCHAR,
        start_date DATE,
        end_date DATE,
        PRIMARY KEY (artist_id, genre_id)
    )
"""

_TABLE_LOCATION = """
    CREATE TABLE IF NOT EXISTS silver.location (
        country_code VARCHAR(2) PRIMARY KEY,
        country_name VARCHAR,
        region VARCHAR(5)
    )
"""


def create_silver_tables(conn: duckdb.DuckDBPyConnection) -> None:
    """Create cleaned and validated tables in the silver schema.

    Args:
        conn: DuckDB connection.
    """
    for sql in (_TABLE_ARTIST, _TABLE_GENRE, _TABLE_ARTIST_GENRE, _TABLE_LOCATION):
        conn.execute(sql)
