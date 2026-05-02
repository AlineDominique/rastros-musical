"""Integration tests for DuckDB database operations and connectivity."""

import pytest

from app.db.database import DuckDBManager


@pytest.fixture
def temp_db(tmp_path):
    """Creates a temporary database for testing.

    Using tmp_path (a built-in pytest fixture) ensures the DB is
    created in a safe, temporary location that is cleaned up after.
    """
    db_file = tmp_path / "test_music.db"
    manager = DuckDBManager(db_path=str(db_file))
    return manager


def test_duckdb_connection(temp_db):
    """Tests connection using the temporary database fixture."""
    with temp_db.get_connection() as conn:
        res = conn.execute("SELECT 1").fetchone()
        assert res[0] == 1
