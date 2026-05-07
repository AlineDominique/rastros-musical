"""Tests for the ingestion runner."""

from unittest.mock import MagicMock, patch

import pytest

from app.ingestion.ingestion_runner import run_ingestion


@pytest.fixture
def mocks():
    """Setup mocked MusicBrainzClient and BronzeLoader."""
    mock_client = MagicMock()
    mock_client.get_genre_id.return_value = "genre-id-123"
    mock_client.search_artists_by_genre.return_value = {"artists": [], "count": 0}
    mock_loader = MagicMock()

    with (
        patch("app.ingestion.ingestion_runner.MusicBrainzClient") as mock_client_class,
        patch("app.ingestion.ingestion_runner.BronzeLoader") as mock_loader_class,
    ):
        mock_client_class.return_value = mock_client
        mock_loader_class.return_value = mock_loader

        yield mock_client, mock_loader


# ===== Testes de quantidade de chamadas =====


@pytest.mark.parametrize(
    "method,expected_count",
    [
        ("search_artists_by_genre", 21),
        ("insert_genre", 21),
    ],
)
def test_run_ingestion_calls_method(mocks, method, expected_count):
    """Should call the expected method for all 21 genres."""
    mock_client, mock_loader = mocks

    run_ingestion()

    if method.startswith("insert"):
        assert getattr(mock_loader, method).call_count == expected_count
    else:
        assert getattr(mock_client, method).call_count == expected_count


def test_run_ingestion_inserts_artists_and_relations(mocks):
    """Should insert artists and artist-genre relations."""
    mock_client, mock_loader = mocks
    mock_client.search_artists_by_genre.return_value = {
        "artists": [{"id": "artist-1", "name": "Test", "country": "BR"}],
        "count": 1,
    }

    run_ingestion()

    assert mock_loader.insert_artist.call_count == 21
    assert mock_loader.insert_artist_genre.call_count == 21


# ===== Testes de logging =====


def test_run_ingestion_logs_start_and_completion(mocks):
    """Should log start and completion messages."""
    with patch("app.ingestion.ingestion_runner.logger") as mock_logger:
        run_ingestion()

        start_call = mock_logger.info.call_args_list[0]
        assert "Starting ingestion" in start_call[0][0]

        end_call = mock_logger.info.call_args_list[-1]
        assert "Ingestion complete" in end_call[0][0]


def test_run_ingestion_logs_artist_count(mocks):
    """Should log artist count for each genre."""
    mock_client, _ = mocks
    mock_client.search_artists_by_genre.return_value = {"artists": [], "count": 150}

    with patch("app.ingestion.ingestion_runner.logger.info") as mock_info:
        run_ingestion()

        found = any(
            "Found" in str(call) and "artists for genre" in str(call)
            for call in mock_info.call_args_list
        )
        assert found, "Expected 'Found X artists for genre' log not found"


@pytest.mark.parametrize(
    "failure_type",
    [
        "artist_insert",
        "genre_process",
    ],
)
def test_run_ingestion_logs_error(mocks, failure_type):
    """Should log error on failures."""
    mock_client, mock_loader = mocks

    if failure_type == "artist_insert":
        mock_client.search_artists_by_genre.return_value = {
            "artists": [{"id": "bad", "name": None}],
            "count": 1,
        }
        mock_loader.insert_artist.side_effect = Exception("DB error")
    else:
        mock_client.search_artists_by_genre.side_effect = Exception("API error")

    with patch("app.ingestion.ingestion_runner.logger.error") as mock_error:
        run_ingestion()

        assert mock_error.call_count >= 1
