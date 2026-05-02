"""Database module for DuckDB connection management and persistence."""

import os
from collections.abc import Generator
from contextlib import contextmanager

import duckdb

DATABASE_PATH = "data/rastros_musical.db"


class DuckDBManager:
    """Manages DuckDB connections and persistence."""

    def __init__(self, db_path: str = DATABASE_PATH) -> None:
        """Initializes the manager and ensures the data directory exists.

        Args:
            db_path (str): Path to the .db file.
        """
        self.db_path = db_path
        # Create the directory if it doesn't exist to prevent IOErrors
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    @contextmanager
    def get_connection(self) -> Generator[duckdb.DuckDBPyConnection, None, None]:
        """Creates a thread-safe connection to DuckDB.

        Yields:
            duckdb.DuckDBPyConnection: An active DuckDB connection.
        """
        conn = duckdb.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()


db_manager = DuckDBManager()
