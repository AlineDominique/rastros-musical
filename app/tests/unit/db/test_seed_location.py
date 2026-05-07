"""Tests for seed_location."""

from app.db.seed_location import seed_location


def test_seed_location_populates_table(conn):
    """Should populate silver.location with country data."""
    conn.execute("""
        CREATE TABLE silver.location (
            country_code VARCHAR(2) PRIMARY KEY,
            country_name VARCHAR,
            region VARCHAR(5),
            latitude DOUBLE,
            longitude DOUBLE
        )
    """)

    seed_location(conn)

    count = conn.execute("SELECT COUNT(*) FROM silver.location").fetchone()[0]
    assert count == 32

    brazil = conn.execute(
        "SELECT * FROM silver.location WHERE country_code = 'BR'"
    ).fetchone()
    assert brazil[0] == "BR"
    assert brazil[1] == "Brazil"
    assert brazil[2] == "Latam"
    assert brazil[3] == -10.0
    assert brazil[4] == -55.0
