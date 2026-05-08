"""Google Trends client for tracking genre search interest over time."""

from pandas import DataFrame
from pytrends.request import TrendReq


class GoogleTrendsClient:
    """Client for fetching search interest data from Google Trends."""

    def __init__(self, timeout: int = 30) -> None:
        """Initialize the Google Trends client.

        Args:
            timeout: Connection timeout in seconds.
        """
        self.timeout = timeout
        self._client = TrendReq(timeout=timeout)

    def get_interest_over_time(self, keywords: list[str], geo: str = "") -> "DataFrame":
        """Fetch interest over time for given keywords in a country.

        Args:
            keywords: List of search terms (max 5).
            geo: ISO 3166-1 alpha-2 country code (e.g., 'BR', 'JP').

        Returns:
            Pandas DataFrame with interest values indexed by date.
        """
        self._client.build_payload(
            kw_list=keywords,
            geo=geo,
            timeframe="all",
        )
        return self._client.interest_over_time()
