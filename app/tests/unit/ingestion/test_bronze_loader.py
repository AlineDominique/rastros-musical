"""Tests for bronze layer loading."""

import pytest

from app.ingestion.bronze_loader import BronzeLoader


@pytest.fixture(autouse=True)
def setup_tables(conn):
    """Create tables needed for bronze loader tests."""
    conn.execute("""
        CREATE TABLE bronze.artist_raw (
            artist_id VARCHAR PRIMARY KEY,
            name VARCHAR,
            country_code VARCHAR(2),
            latitude DOUBLE,
            longitude DOUBLE,
            ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE bronze.genre_raw (
            genre_id VARCHAR PRIMARY KEY,
            name VARCHAR,
            parent_genre_id INTEGER,
            ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE bronze.artist_genre_raw (
            artist_id VARCHAR,
            genre_id VARCHAR,
            start_date VARCHAR,
            end_date VARCHAR,
            ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (artist_id, genre_id)
        )
    """)


def test_insert_artist(conn):
    """Should insert a raw artist record."""
    loader = BronzeLoader(conn)
    artist = {"artist_id": "1", "name": "Chico Buarque", "country_code": "BR"}

    loader.insert_artist(artist)

    result = conn.execute(
        "SELECT * FROM bronze.artist_raw WHERE artist_id = '1'"
    ).fetchone()
    assert result[0] == "1"
    assert result[1] == "Chico Buarque"
    assert result[2] == "BR"


def test_insert_artist_with_coordinates(conn):
    """Should insert artist with latitude and longitude."""
    loader = BronzeLoader(conn)
    artist = {
        "artist_id": "2",
        "name": "Caetano Veloso",
        "country_code": "BR",
        "latitude": -14.235,
        "longitude": -51.925,
    }

    loader.insert_artist(artist)

    result = conn.execute(
        "SELECT latitude, longitude FROM bronze.artist_raw WHERE artist_id = '2'"
    ).fetchone()
    assert result[0] == -14.235
    assert result[1] == -51.925


def test_insert_genre(conn):
    """Should insert a raw genre record."""
    loader = BronzeLoader(conn)
    genre = {"genre_id": "genre-samba", "name": "Samba"}

    loader.insert_genre(genre)

    result = conn.execute(
        "SELECT * FROM bronze.genre_raw WHERE genre_id = 'genre-samba'"
    ).fetchone()
    assert result[0] == "genre-samba"
    assert result[1] == "Samba"


def test_insert_artist_genre(conn):
    """Should insert an artist-genre relation with all fields."""
    loader = BronzeLoader(conn)
    relation = {
        "artist_id": "artist-1",
        "genre_id": "genre-samba",
        "start_date": "1988",
        "end_date": None,
    }

    loader.insert_artist_genre(relation)
    sql = (
        "SELECT * FROM bronze.artist_genre_raw "
        "WHERE artist_id = 'artist-1' AND genre_id = 'genre-samba'"
    )
    result = conn.execute(sql).fetchone()
    assert result[0] == "artist-1"
    assert result[1] == "genre-samba"
    assert result[2] == "1988"
    assert result[3] is None


def test_insert_artist_ignores_duplicate(conn):
    """Should ignore duplicate artist IDs."""
    loader = BronzeLoader(conn)
    artist = {"artist_id": "1", "name": "Chico Buarque", "country_code": "BR"}

    loader.insert_artist(artist)
    loader.insert_artist(artist)  # duplicata

    count = conn.execute(
        "SELECT COUNT(*) FROM bronze.artist_raw WHERE artist_id = '1'"
    ).fetchone()[0]
    assert count == 1


def test_insert_genre_ignores_duplicate(conn):
    """Should ignore duplicate genre IDs."""
    loader = BronzeLoader(conn)
    genre = {"genre_id": "genre-samba", "name": "Samba"}

    loader.insert_genre(genre)
    loader.insert_genre(genre)

    count = conn.execute(
        "SELECT COUNT(*) FROM bronze.genre_raw WHERE genre_id = 'genre-samba'"
    ).fetchone()[0]
    assert count == 1


def test_insert_artist_genre_ignores_duplicate(conn):
    """Should ignore duplicate artist-genre relations."""
    loader = BronzeLoader(conn)
    relation = {"artist_id": "1", "genre_id": "genre-samba", "start_date": "1988"}

    loader.insert_artist_genre(relation)
    loader.insert_artist_genre(relation)

    count = conn.execute(
        "SELECT COUNT(*) FROM bronze.artist_genre_raw "
        "WHERE artist_id = '1' AND genre_id = 'genre-samba'"
    ).fetchone()[0]
    assert count == 1
