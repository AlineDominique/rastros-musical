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
    conn.execute("CREATE SCHEMA IF NOT EXISTS gold;")


def test_genre_first_appearance(conn):
    """Should create first appearance records per genre and country."""
    conn.execute(
        "INSERT INTO silver.artist VALUES ('a1', 'Chico', 'BR', -10.0, -55.0, 'Latam')"
    )
    conn.execute(
        "INSERT INTO silver.artist VALUES ("
        "'a2', 'Caetano', 'BR', -10.0, -55.0, 'Latam')"
    )
    conn.execute("INSERT INTO silver.genre VALUES ('genre-samba', 'Samba')")
    conn.execute(
        "INSERT INTO silver.artist_genre VALUES ("
        "'a1', 'genre-samba', '1970-03-15', NULL)"
    )
    conn.execute(
        "INSERT INTO silver.artist_genre VALUES ("
        "'a2', 'genre-samba', '1975-01-01', NULL)"
    )
    conn.execute(
        "INSERT INTO silver.location VALUES ('BR', 'Brazil', 'Latam', -10.0, -55.0)"
    )

    loader = GoldLoader(conn)
    loader.load_genre_first_appearance()

    result = conn.execute(
        "SELECT genre, target_country, target_lat, target_lon, first_year "
        "FROM gold.genre_first_appearance"
    ).fetchone()

    assert result[0] == "Samba"
    assert result[1] == "BR"
    assert result[2] == -10.0
    assert result[3] == -55.0
    assert result[4] == 1970  # primeira aparição: 1970


def test_genre_first_appearance_multiple_countries(conn):
    """Should create records for each country a genre appeared in."""
    conn.execute(
        "INSERT INTO silver.artist VALUES ('a1', 'Chico', 'BR', -10.0, -55.0, 'Latam')"
    )
    conn.execute(
        "INSERT INTO silver.artist VALUES ("
        "'a3', 'Artist JP', 'JP', 36.0, 138.0, 'Asia')"
    )
    conn.execute("INSERT INTO silver.genre VALUES ('genre-samba', 'Samba')")
    conn.execute(
        "INSERT INTO silver.artist_genre VALUES ("
        "'a1', 'genre-samba', '1970-01-01', NULL)"
    )
    conn.execute(
        "INSERT INTO silver.artist_genre VALUES ("
        "'a3', 'genre-samba', '1985-01-01', NULL)"
    )
    conn.execute(
        "INSERT INTO silver.location VALUES ('BR', 'Brazil', 'Latam', -10.0, -55.0)"
    )
    conn.execute(
        "INSERT INTO silver.location VALUES ('JP', 'Japan', 'Asia', 36.0, 138.0)"
    )

    loader = GoldLoader(conn)
    loader.load_genre_first_appearance()

    results = conn.execute(
        "SELECT target_country, first_year "
        "FROM gold.genre_first_appearance ORDER BY first_year"
    ).fetchall()

    assert len(results) == 2
    assert results[0][0] == "BR"
    assert results[0][1] == 1970
    assert results[1][0] == "JP"
    assert results[1][1] == 1985
