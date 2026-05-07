"""Tests for the run_ingestion script."""

from unittest.mock import MagicMock, patch

from app.run_ingestion import main


def test_main_calls_setup_and_ingestion():
    """Should setup database and run ingestion."""
    with (
        patch("app.run_ingestion.db_manager") as mock_db,
        patch("app.run_ingestion.setup_database") as mock_setup,
        patch("app.run_ingestion.run_ingestion") as mock_ingestion,
    ):
        mock_conn = MagicMock()
        mock_db.get_connection.return_value.__enter__.return_value = mock_conn

        main()

        mock_setup.assert_called_once_with(mock_conn)
        mock_ingestion.assert_called_once()
