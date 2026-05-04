"""Database setup — creates all schemas and tables."""

import duckdb

from app.db.bronze import create_bronze_tables
from app.db.database import db_manager
from app.db.silver import create_silver_tables

_SCHEMAS = ("bronze", "silver", "gold")


def setup_database(conn: duckdb.DuckDBPyConnection = None) -> None:
    """Initialize the database with all schemas and tables.

    Args:
        conn: DuckDB connection. If None, uses the default db_manager.
              The caller is responsible for closing if provided externally.
    """
    if conn is None:
        with db_manager.get_connection() as conn:
            _create_schemas(conn)
            _create_tables(conn)
    else:
        _create_schemas(conn)
        _create_tables(conn)


def _create_schemas(conn: duckdb.DuckDBPyConnection) -> None:
    """Create Medallion schemas."""
    for schema in _SCHEMAS:
        conn.execute(f"CREATE SCHEMA IF NOT EXISTS {schema};")


def _create_tables(conn: duckdb.DuckDBPyConnection) -> None:
    """Create all tables across layers."""
    create_bronze_tables(conn)
    create_silver_tables(conn)
