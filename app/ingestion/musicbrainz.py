import time
from typing import Any

import httpx


class MusicBrainzClient:
    """Client for the MusicBrainz REST API."""

    def __init__(self, user_agent: str = "RastrosMusical/0.1") -> None:
        """Initialize the client.

        Args:
            user_agent: User-Agent header for MusicBrainz requests.
        """
        self.base_url = "https://musicbrainz.org/ws/2"
        self.user_agent = user_agent
        self._client = httpx.Client(
            base_url=self.base_url,
            headers={"User-Agent": self.user_agent},
        )
        self._last_request_time = 0.0

    def _rate_limit(self) -> None:
        """Ensure at least 1 second between requests (MusicBrainz limit)."""
        elapsed = time.time() - self._last_request_time
        if elapsed < 1:
            time.sleep(1 - elapsed)
        self._last_request_time = time.time()
    

    def search_artists_by_genre(
        self, genre: str, limit: int = 100, offset: int = 0
    ) -> dict[str, Any]:
        """Search for artists by genre tag.

        Args:
            genre: Music genre to search for.
            limit: Maximum results per page (max 100).
            offset: Pagination offset.

        Returns:
            JSON response with artists list and count.
        """
        self._rate_limit()
        response = self._client.get(
            "/artist",
            params={
                "query": f'tag:"{genre}"',
                "limit": limit,
                "offset": offset,
                "fmt": "json",
            },
        )
        response.raise_for_status()
        return response.json()