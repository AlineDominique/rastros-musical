"""Tests for gold layer loading."""

import pytest

from app.ingestion.gold_loader import GoldLoader


@pytest.fixture(autouse=True)
def setup_tables(conn):
    """Create tables needed for gold loader tests."""
    conn.execute("""
        CREATE TABLE silver.artist (
            artist_id VARCHAR PRIMARY KEY, name VARCHAR NOT NULL,
            country_code VARCHAR(2), latitude DOUBLE, longitude DOUBLE,
            region VARCHAR(5)
        )
    """)
    conn.execute("""
        CREATE TABLE silver.genre (
            genre_id VARCHAR PRIMARY KEY, name VARCHAR NOT NULL
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
    conn.execute("""
        CREATE TABLE silver.genre_propagation (
            genre VARCHAR NOT NULL,
            country_code VARCHAR(2) NOT NULL,
            first_year INTEGER,
            PRIMARY KEY (genre, country_code)
        )
    """)
    conn.execute("CREATE SCHEMA IF NOT EXISTS gold;")


def test_load_genre_first_appearance(conn):
    """Should create first appearance records for curated origins."""
    conn.execute(
        "INSERT INTO silver.artist "
        "VALUES ('a1', 'Samba Origin', 'BR', -10.0, -55.0, 'Latam')"
    )
    conn.execute("INSERT INTO silver.genre VALUES ('genre-samba', 'samba')")
    conn.execute(
        "INSERT INTO silver.artist_genre "
        "VALUES ('a1', 'genre-samba', '1870-01-01', NULL)"
    )
    conn.execute(
        "INSERT INTO silver.location VALUES ('BR', 'Brazil', 'Latam', -10.0, -55.0)"
    )

    loader = GoldLoader(conn)
    loader.load_genre_first_appearance()
    loader.load_genre_first_appearance()

    result = conn.execute(
        "SELECT genre, target_country, first_year, source FROM "
        "gold.genre_first_appearance"
    ).fetchone()

    assert result[0] == "samba"
    assert result[1] == "BR"
    assert result[2] == 1870
    assert result[3] == "curated_origin"


def test_load_genre_propagation(conn):
    """Should load Google Trends propagation into Gold."""
    conn.execute(
        "INSERT INTO silver.location VALUES ('BR', 'Brazil', 'Latam', -10.0, -55.0)"
    )
    conn.execute("INSERT INTO silver.genre_propagation VALUES ('samba', 'BR', 2006)")

    loader = GoldLoader(conn)
    loader.load_genre_first_appearance()
    loader.load_genre_propagation()

    result = conn.execute(
        "SELECT genre, target_country, first_year, source "
        "FROM gold.genre_first_appearance"
    ).fetchone()

    assert result[0] == "samba"
    assert result[1] == "BR"
    assert result[2] == 2006
    assert result[3] == "google_trends"
