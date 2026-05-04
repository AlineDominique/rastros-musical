"""Shared fixtures for all tests."""

import duckdb
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest_asyncio.fixture
async def client():
    """Async HTTP client for testing."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def conn():
    """In-memory DuckDB connection with bronze and silver schemas."""
    connection = duckdb.connect(":memory:")
    connection.execute("CREATE SCHEMA IF NOT EXISTS bronze;")
    connection.execute("CREATE SCHEMA IF NOT EXISTS silver;")
    connection.execute("CREATE SCHEMA IF NOT EXISTS gold;")
    yield connection
    connection.close()


@pytest.fixture
def tables(conn):
    """Helper to get table names from a schema."""

    def _get_tables(schema: str) -> list[str]:
        return [
            t[0]
            for t in conn.execute(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = ?",
                [schema],
            ).fetchall()
        ]

    return _get_tables


@pytest.fixture
def columns(conn):
    """Helper to get column names from a table."""

    def _get_columns(table_name: str) -> list[str]:
        result = conn.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_name = ?",
            [table_name],
        ).fetchall()
        return [c[0] for c in result]

    return _get_columns
