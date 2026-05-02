"""Integration tests for DuckDB database operations and connectivity."""

import os

from app.db.database import db_manager


def test_duckdb_connection():
    """Verifica se o DuckDB consegue abrir o arquivo e executar SQL básico."""
    with db_manager.get_connection() as conn:
        result = conn.execute("SELECT 1").fetchone()
        assert result[0] == 1


def test_database_file_exists():
    """Verifica se o arquivo .db foi criado na pasta correta."""
    assert os.path.exists("data/rastros_musical.db")
