"""Tests for Google Trends client."""

from unittest.mock import MagicMock, patch

import pytest

from app.ingestion.google_trends import GoogleTrendsClient


@pytest.fixture
def client():
    """Google Trends client instance."""
    return GoogleTrendsClient()


def test_client_has_default_timeout(client):
    """Should have default timeout set."""
    assert client.timeout == 30


def test_get_interest_over_time_returns_dataframe():
    """Should return structured data from Google Trends."""
    mock_pytrends = MagicMock()
    mock_pytrends.interest_over_time.return_value = MagicMock()

    with patch("app.ingestion.google_trends.TrendReq") as mock_trend_req:
        mock_trend_req.return_value = mock_pytrends

        client = GoogleTrendsClient()
        result = client.get_interest_over_time(["samba"], geo="JP")

        assert result is not None
        mock_pytrends.build_payload.assert_called_once_with(
            kw_list=["samba"],
            geo="JP",
            timeframe="all",
        )
