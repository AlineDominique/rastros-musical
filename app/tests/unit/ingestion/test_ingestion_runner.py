"""Tests for the ingestion runner."""

from unittest.mock import MagicMock, patch

import pytest

from app.ingestion.ingestion_runner import run_ingestion


@pytest.fixture
def mocks():
    """Setup mocked BronzeLoader and database."""
    mock_loader = MagicMock()

    with (
        patch("app.ingestion.ingestion_runner.BronzeLoader") as mock_loader_class,
        patch("app.ingestion.ingestion_runner.db_manager") as mock_db,
    ):
        mock_conn = MagicMock()
        mock_db.get_connection.return_value.__enter__.return_value = mock_conn
        mock_loader_class.return_value = mock_loader

        yield mock_loader


def test_run_ingestion_inserts_all_genres(mocks):
    """Should insert all 20 genres."""
    mock_loader = mocks

    run_ingestion()

    assert mock_loader.insert_genre.call_count == 20


def test_run_ingestion_inserts_origin_artists(mocks):
    """Should insert origin artists for each genre."""
    mock_loader = mocks

    run_ingestion()

    assert mock_loader.insert_artist.call_count == 20


def test_run_ingestion_inserts_artist_genre_relations(mocks):
    """Should insert artist-genre relations for each genre."""
    mock_loader = mocks

    run_ingestion()

    assert mock_loader.insert_artist_genre.call_count == 20


def test_run_ingestion_logs_start_and_completion(mocks):
    """Should log start and completion messages."""
    with patch("app.ingestion.ingestion_runner.logger") as mock_logger:
        run_ingestion()

        start_call = mock_logger.info.call_args_list[0]
        assert "Starting ingestion" in start_call[0][0]

        end_call = mock_logger.info.call_args_list[-1]
        assert "Ingestion complete" in end_call[0][0]


def test_run_ingestion_skips_genre_without_origin(mocks):
    """Should skip genre not found in GENRE_ORIGINS."""
    with patch("app.ingestion.ingestion_runner.logger.warning") as mock_warning:
        with patch("app.ingestion.ingestion_runner.ALL_GENRES", ["fake-genre"]):
            run_ingestion()

        mock_warning.assert_called_once()
        assert "No origin data" in mock_warning.call_args[0][0]


def test_run_ingestion_logs_error_on_insert_failure(mocks):
    """Should log error when genre processing fails."""
    mock_loader = mocks
    mock_loader.insert_genre.side_effect = Exception("DB error")

    with patch("app.ingestion.ingestion_runner.logger.error") as mock_error:
        run_ingestion()

        assert mock_error.call_count == 20
