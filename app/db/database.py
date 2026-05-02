"""Database module for DuckDB connection management and persistence."""

from collections.abc import Generator
from contextlib import contextmanager

import duckdb

DATABASE_PATH = "data/rastros_musical.db"


class DuckDBManager:
    """Manages DuckDB connections and persistence.

    Attributes:
        db_path (str): The file path where the DuckDB database is stored.
    """

    def __init__(self, db_path: str = DATABASE_PATH) -> None:
        """Initializes the manager with a specific database path.

        Args:
            db_path (str): Path to the .db file. Defaults to DATABASE_PATH.
        """
        self.db_path = db_path

    @contextmanager
    def get_connection(self) -> Generator[duckdb.DuckDBPyConnection, None, None]:
        """Creates a thread-safe connection to DuckDB using a context manager.

        Yields:
            duckdb.DuckDBPyConnection: An active DuckDB connection object.

        Raises:
            duckdb.Error: If the connection to the database fails.
        """
        conn = duckdb.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()


# Global instance for API usage
db_manager = DuckDBManager()
