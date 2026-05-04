"""Tests for database setup."""

from unittest.mock import MagicMock, patch

from app.db.setup import setup_database


def test_setup_database_uses_db_manager_when_no_conn():
    """Should use db_manager when no connection is provided."""
    mock_conn = MagicMock()
    mock_db_manager = MagicMock()
    mock_db_manager.get_connection.return_value.__enter__.return_value = mock_conn

    with patch("app.db.setup.db_manager", mock_db_manager):
        setup_database()

    mock_db_manager.get_connection.assert_called_once()


def test_setup_database_creates_all_schemas(conn):
    """Should create bronze, silver and gold schemas."""
    setup_database(conn)

    schemas = conn.execute(
        "SELECT schema_name FROM information_schema.schemata"
    ).fetchall()
    schema_names = [s[0] for s in schemas]

    assert "bronze" in schema_names
    assert "silver" in schema_names
    assert "gold" in schema_names


def test_setup_database_creates_bronze_tables(conn, tables):
    """Should create raw ingestion tables via setup."""
    setup_database(conn)

    bronze_tables = tables("bronze")
    assert "artist_raw" in bronze_tables
    assert "genre_raw" in bronze_tables
    assert "artist_genre_raw" in bronze_tables


def test_setup_database_creates_silver_tables(conn, tables):
    """Should create cleaned tables via setup."""
    setup_database(conn)

    silver_tables = tables("silver")
    assert "artist" in silver_tables
    assert "genre" in silver_tables
    assert "artist_genre" in silver_tables
    assert "location" in silver_tables
