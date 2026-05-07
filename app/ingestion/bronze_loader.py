"""Load raw data into the Bronze layer."""

from typing import Any

import duckdb


class BronzeLoader:
    """Loads raw data from ingestion into the Bronze layer."""

    def __init__(self, conn: duckdb.DuckDBPyConnection) -> None:
        """Initialize with a DuckDB connection.

        Args:
            conn: Active DuckDB connection.
        """
        self.conn = conn

    def insert_artist(self, artist: dict[str, Any]) -> None:
        """Insert a raw artist record.

        Args:
            artist: Dictionary with artist_id, name, country_code,
                    and optionally latitude and longitude.
        """
        self.conn.execute(
            """
            INSERT OR IGNORE INTO bronze.artist_raw (
            artist_id, name, country_code, latitude, longitude)
            VALUES (?, ?, ?, ?, ?)
            """,
            [
                artist["artist_id"],
                artist["name"],
                artist.get("country_code", ""),
                artist.get("latitude"),
                artist.get("longitude"),
            ],
        )

    def insert_genre(self, genre: dict[str, Any]) -> None:
        """Insert a raw genre record.

        Args:
            genre: Dictionary with genre_id, name, and optionally parent_genre_id.
        """
        self.conn.execute(
            """
            INSERT OR IGNORE INTO bronze.genre_raw (
            genre_id, name, parent_genre_id)
            VALUES (?, ?, ?)
            """,
            [genre["genre_id"], genre["name"], genre.get("parent_genre_id")],
        )

    def insert_artist_genre(self, relation: dict[str, Any]) -> None:
        """Insert a raw artist-genre relation."""
        self.conn.execute(
            """
        INSERT OR IGNORE INTO bronze.artist_genre_raw (
        artist_id, genre_id, start_date, end_date)
        VALUES (?, ?, ?, ?)
        """,
            [
                relation["artist_id"],
                relation["genre_id"],
                relation.get("start_date"),
                relation.get("end_date"),
            ],
        )
