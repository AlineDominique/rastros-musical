"""Tests for silver layer loading."""

from unittest.mock import patch

import pytest

from app.ingestion.silver_loader import SilverLoader, normalize_date


@pytest.fixture(autouse=True)
def setup_tables(conn):
    """Create tables needed for silver loader tests."""
    conn.execute("""
        CREATE TABLE bronze.artist_raw (
            artist_id VARCHAR, name VARCHAR, country_code VARCHAR(2),
            latitude DOUBLE, longitude DOUBLE,
            ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE bronze.genre_raw (
            genre_id VARCHAR, name VARCHAR, parent_genre_id INTEGER,
            ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE bronze.artist_genre_raw (
            artist_id VARCHAR, genre_id VARCHAR,
            start_date VARCHAR, end_date VARCHAR,
            ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE silver.artist (
            artist_id VARCHAR PRIMARY KEY, name VARCHAR NOT NULL,
            country_code VARCHAR(2), latitude DOUBLE, longitude DOUBLE,
            region VARCHAR(5), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE silver.genre (
            genre_id VARCHAR PRIMARY KEY, name VARCHAR NOT NULL,
            parent_genre_id INTEGER, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE silver.artist_genre (
            artist_id VARCHAR, genre_id VARCHAR,
            start_date DATE, end_date DATE,
            PRIMARY KEY (artist_id, genre_id)
        )
    """)
    conn.execute("""
        CREATE TABLE silver.location (
            country_code VARCHAR(2) PRIMARY KEY, country_name VARCHAR,
            region VARCHAR(5), latitude DOUBLE, longitude DOUBLE
        )
    """)


def test_normalize_date_full():
    """Should keep YYYY-MM-DD unchanged."""
    assert normalize_date("1988-03-15") == "1988-03-15"


def test_normalize_date_year_month():
    """Should pad YYYY-MM to YYYY-MM-DD."""
    assert normalize_date("1988-03") == "1988-03-01"


def test_normalize_date_year_only():
    """Should pad YYYY to YYYY-01-01."""
    assert normalize_date("1988") == "1988-01-01"


def test_normalize_date_none():
    """Should return None for None input."""
    assert normalize_date(None) is None


def test_normalize_date_empty():
    """Should return None for empty string."""
    assert normalize_date("") is None


def test_load_artists(conn):
    """Should load artists from bronze to silver with region."""
    conn.execute(
        "INSERT INTO silver.location VALUES ('BR', 'Brazil', 'Latam', -10.0, -55.0)"
    )
    sql_insert_artist_raw = (
        "INSERT INTO bronze.artist_raw "
        "VALUES ('artist-1', 'Chico Buarque', 'BR', NULL, NULL, CURRENT_TIMESTAMP)"
    )
    conn.execute(sql_insert_artist_raw)

    loader = SilverLoader(conn)
    loader.load_artists()

    result = conn.execute(
        "SELECT artist_id, name, country_code, region FROM silver.artist"
    ).fetchone()
    assert result[0] == "artist-1"
    assert result[1] == "Chico Buarque"
    assert result[2] == "BR"
    assert result[3] == "Latam"


def test_load_genres(conn):
    """Should load genres from bronze to silver."""
    sql_insert_bronze_genre_raw = (
        "INSERT INTO bronze.genre_raw "
        "VALUES ('genre-samba', 'Samba', NULL, CURRENT_TIMESTAMP)"
    )
    conn.execute(sql_insert_bronze_genre_raw)

    loader = SilverLoader(conn)
    loader.load_genres()

    result = conn.execute("SELECT genre_id, name FROM silver.genre").fetchone()
    assert result[0] == "genre-samba"
    assert result[1] == "Samba"


def test_load_artist_genres(conn):
    """Should load artist-genre relations with normalized dates."""
    sql_insert_genre_raw = (
        "INSERT INTO bronze.artist_genre_raw "
        "VALUES ('artist-1', 'genre-samba', '1970', NULL, CURRENT_TIMESTAMP)"
    )
    conn.execute(sql_insert_genre_raw)

    loader = SilverLoader(conn)
    loader.load_artist_genres()

    result = conn.execute(
        "SELECT artist_id, genre_id, start_date FROM silver.artist_genre"
    ).fetchone()
    assert result[0] == "artist-1"
    assert result[1] == "genre-samba"
    assert str(result[2]) == "1970-01-01"


def test_load_genre_propagation(conn):
    """Should load genre propagation data from Google Trends."""
    conn.execute(
        "INSERT INTO silver.location VALUES ('BR', 'Brazil', 'Latam', -10.0, -55.0)"
    )
    conn.execute("""
        CREATE TABLE silver.genre_propagation (
            genre VARCHAR NOT NULL,
            country_code VARCHAR(2) NOT NULL,
            first_year INTEGER,
            PRIMARY KEY (genre, country_code)
        )
    """)

    with patch("app.ingestion.silver_loader.build_propagation_data") as mock_build:
        mock_build.return_value = [
            {"genre": "samba", "country_code": "BR", "first_year": 2006},
            {"genre": "samba", "country_code": "JP", "first_year": 2010},
        ]

        loader = SilverLoader(conn)
        loader.load_genre_propagation(["BR", "JP"])

    results = conn.execute(
        "SELECT * FROM silver.genre_propagation ORDER BY first_year"
    ).fetchall()
    assert len(results) == 2
    assert results[0][0] == "samba"
    assert results[0][1] == "BR"
    assert results[0][2] == 2006
