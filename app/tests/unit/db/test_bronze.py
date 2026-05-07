"""Tests for bronze layer tables."""

from app.db.bronze import create_bronze_tables


def test_create_bronze_tables_creates_all_tables(conn, tables):
    """Should create all raw ingestion tables."""
    create_bronze_tables(conn)

    bronze_tables = tables("bronze")
    assert "artist_raw" in bronze_tables
    assert "genre_raw" in bronze_tables
    assert "artist_genre_raw" in bronze_tables


def test_artist_raw_has_required_columns(conn, columns):
    """Should have expected columns for artist_raw."""
    create_bronze_tables(conn)

    artist_columns = columns("artist_raw")
    assert "artist_id" in artist_columns
    assert "name" in artist_columns
    assert "country_code" in artist_columns
    assert "latitude" in artist_columns
    assert "longitude" in artist_columns
    assert "ingested_at" in artist_columns


def test_genre_raw_has_required_columns(conn, columns):
    """Should have expected columns for genre_raw."""
    create_bronze_tables(conn)

    genre_columns = columns("genre_raw")
    assert "genre_id" in genre_columns
    assert "name" in genre_columns
    assert "parent_genre_id" in genre_columns
    assert "ingested_at" in genre_columns


def test_artist_genre_raw_has_required_columns(conn, columns):
    """Should have expected columns for artist_genre_raw."""
    create_bronze_tables(conn)

    ag_columns = columns("artist_genre_raw")
    assert "artist_id" in ag_columns
    assert "genre_id" in ag_columns
    assert "start_date" in ag_columns
    assert "end_date" in ag_columns
    assert "ingested_at" in ag_columns
