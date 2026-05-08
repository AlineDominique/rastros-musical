"""Tests for Google Trends integration with the pipeline."""

from unittest.mock import MagicMock, patch

import pandas as pd

from app.ingestion.trends_integration import (
    build_propagation_data,
    find_first_significant_year,
)


def test_find_first_significant_year_returns_correct_year():
    """Should return the first year with significant search interest."""
    mock_df = pd.DataFrame(
        {"samba": [0, 0, 20, 50, 80]},
        index=pd.date_range("2004-01-01", periods=5, freq="YS"),
    )

    result = find_first_significant_year(mock_df, threshold=10)

    assert result == 2006


def test_find_first_significant_year_returns_none_when_no_data():
    """Should return None when no value exceeds threshold."""
    mock_df = pd.DataFrame(
        {"samba": [0, 0, 0]},
        index=pd.date_range("2004-01-01", periods=3, freq="YS"),
    )

    result = find_first_significant_year(mock_df, threshold=10)

    assert result is None


def test_find_first_significant_year_handles_empty_dataframe():
    """Should return None for empty DataFrame."""
    mock_df = pd.DataFrame()

    result = find_first_significant_year(mock_df, threshold=10)

    assert result is None


def test_build_propagation_data_returns_countries():
    """Should return list of countries where genre was searched."""
    with patch(
        "app.ingestion.trends_integration.GoogleTrendsClient"
    ) as mock_client_class:
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        mock_df = pd.DataFrame(
            {"samba": [0, 0, 30, 60]},
            index=pd.date_range("2004-01-01", periods=4, freq="YS"),
        )
        mock_client.get_interest_over_time.return_value = mock_df

        result = build_propagation_data("samba", ["BR", "JP"])

        assert len(result) == 2
        assert result[0]["genre"] == "samba"
        assert result[0]["first_year"] == 2006


def test_build_propagation_data_skips_no_data():
    """Should skip countries with no significant interest."""
    with patch(
        "app.ingestion.trends_integration.GoogleTrendsClient"
    ) as mock_client_class:
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        mock_df = pd.DataFrame()
        mock_client.get_interest_over_time.return_value = mock_df

        result = build_propagation_data("samba", ["XX"])

        assert len(result) == 0


def test_build_propagation_data_handles_exception():
    """Should skip country when API call fails."""
    with patch(
        "app.ingestion.trends_integration.GoogleTrendsClient"
    ) as mock_client_class:
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_client.get_interest_over_time.side_effect = Exception("API error")

        result = build_propagation_data("samba", ["BR"])

        assert len(result) == 0
