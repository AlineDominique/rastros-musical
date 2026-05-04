"""Tests for silver layer tables."""

from app.db.silver import create_silver_tables


def test_create_silver_tables_creates_all_tables(conn, tables):
    """Should create all cleaned tables."""
    create_silver_tables(conn)

    silver_tables = tables("silver")
    assert "artist" in silver_tables
    assert "genre" in silver_tables
    assert "artist_genre" in silver_tables
    assert "location" in silver_tables


def test_artist_has_required_columns(conn, columns):
    """Should have expected columns for artist."""
    create_silver_tables(conn)

    artist_columns = columns("artist")
    assert "artist_id" in artist_columns
    assert "name" in artist_columns
    assert "country_code" in artist_columns
    assert "latitude" in artist_columns
    assert "longitude" in artist_columns
    assert "region" in artist_columns
    assert "created_at" in artist_columns


def test_genre_has_required_columns(conn, columns):
    """Should have expected columns for genre."""
    create_silver_tables(conn)

    genre_columns = columns("genre")
    assert "genre_id" in genre_columns
    assert "name" in genre_columns
    assert "parent_genre_id" in genre_columns
    assert "created_at" in genre_columns


def test_artist_genre_has_required_columns(conn, columns):
    """Should have expected columns for artist_genre."""
    create_silver_tables(conn)

    ag_columns = columns("artist_genre")
    assert "artist_id" in ag_columns
    assert "genre_id" in ag_columns
    assert "start_date" in ag_columns
    assert "end_date" in ag_columns


def test_location_has_required_columns(conn, columns):
    """Should have expected columns for location."""
    create_silver_tables(conn)

    loc_columns = columns("location")
    assert "country_code" in loc_columns
    assert "country_name" in loc_columns
    assert "region" in loc_columns
