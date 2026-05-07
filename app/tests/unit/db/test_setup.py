"""Tests for database setup."""

from unittest.mock import MagicMock, patch

from app.db.setup import load_all, setup_all, setup_database


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


def test_setup_all_calls_setup_and_seed():
    """Should call setup_database and seed_location."""
    with (
        patch("app.db.setup.setup_database") as mock_setup,
        patch("app.db.setup.seed_location") as mock_seed,
        patch("app.db.setup.db_manager") as mock_db,
    ):
        mock_conn = MagicMock()
        mock_db.get_connection.return_value.__enter__.return_value = mock_conn

        setup_all()

        mock_setup.assert_called_once_with(mock_conn)
        mock_seed.assert_called_once_with(mock_conn)


def test_load_all_clears_and_loads_layers():
    """Should clear Silver, load Silver, then load Gold."""
    with (
        patch("app.db.setup.SilverLoader") as mock_silver_class,
        patch("app.db.setup.GoldLoader") as mock_gold_class,
        patch("app.db.setup.db_manager") as mock_db,
    ):
        mock_conn = MagicMock()
        mock_db.get_connection.return_value.__enter__.return_value = mock_conn
        mock_silver = MagicMock()
        mock_gold = MagicMock()
        mock_silver_class.return_value = mock_silver
        mock_gold_class.return_value = mock_gold

        load_all()

        assert mock_conn.execute.call_count >= 4
        mock_silver.load_artists.assert_called_once()
        mock_silver.load_genres.assert_called_once()
        mock_silver.load_artist_genres.assert_called_once()
        mock_gold.load_genre_first_appearance.assert_called_once()
