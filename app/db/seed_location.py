"""Seed the silver.location table with country data."""

import duckdb

_LOCATIONS = [
    # Latin America
    {"code": "AR", "name": "Argentina", "region": "Latam", "lat": -34.0, "lon": -64.0},
    {"code": "BO", "name": "Bolivia", "region": "Latam", "lat": -17.0, "lon": -65.0},
    {"code": "BR", "name": "Brazil", "region": "Latam", "lat": -10.0, "lon": -55.0},
    {"code": "CL", "name": "Chile", "region": "Latam", "lat": -30.0, "lon": -71.0},
    {"code": "CO", "name": "Colombia", "region": "Latam", "lat": 4.0, "lon": -72.0},
    {"code": "CR", "name": "Costa Rica", "region": "Latam", "lat": 10.0, "lon": -84.0},
    {"code": "CU", "name": "Cuba", "region": "Latam", "lat": 21.5, "lon": -80.0},
    {
        "code": "DO",
        "name": "Dominican Republic",
        "region": "Latam",
        "lat": 19.0,
        "lon": -70.67,
    },
    {"code": "EC", "name": "Ecuador", "region": "Latam", "lat": -2.0, "lon": -77.5},
    {"code": "GT", "name": "Guatemala", "region": "Latam", "lat": 15.5, "lon": -90.25},
    {"code": "HN", "name": "Honduras", "region": "Latam", "lat": 15.0, "lon": -86.5},
    {"code": "MX", "name": "Mexico", "region": "Latam", "lat": 23.0, "lon": -102.0},
    {"code": "NI", "name": "Nicaragua", "region": "Latam", "lat": 13.0, "lon": -85.0},
    {"code": "PA", "name": "Panama", "region": "Latam", "lat": 9.0, "lon": -80.0},
    {"code": "PE", "name": "Peru", "region": "Latam", "lat": -10.0, "lon": -76.0},
    {"code": "PR", "name": "Puerto Rico", "region": "Latam", "lat": 18.2, "lon": -66.5},
    {"code": "PY", "name": "Paraguay", "region": "Latam", "lat": -23.0, "lon": -58.0},
    {
        "code": "SV",
        "name": "El Salvador",
        "region": "Latam",
        "lat": 13.83,
        "lon": -88.92,
    },
    {"code": "UY", "name": "Uruguay", "region": "Latam", "lat": -33.0, "lon": -56.0},
    {"code": "VE", "name": "Venezuela", "region": "Latam", "lat": 8.0, "lon": -66.0},
    # Asia
    {"code": "CN", "name": "China", "region": "Asia", "lat": 35.0, "lon": 105.0},
    {"code": "HK", "name": "Hong Kong", "region": "Asia", "lat": 22.3, "lon": 114.2},
    {"code": "ID", "name": "Indonesia", "region": "Asia", "lat": -5.0, "lon": 120.0},
    {"code": "IN", "name": "India", "region": "Asia", "lat": 20.0, "lon": 77.0},
    {"code": "JP", "name": "Japan", "region": "Asia", "lat": 36.0, "lon": 138.0},
    {"code": "KR", "name": "South Korea", "region": "Asia", "lat": 37.0, "lon": 127.5},
    {"code": "MY", "name": "Malaysia", "region": "Asia", "lat": 2.5, "lon": 112.5},
    {"code": "PH", "name": "Philippines", "region": "Asia", "lat": 13.0, "lon": 122.0},
    {"code": "SG", "name": "Singapore", "region": "Asia", "lat": 1.37, "lon": 103.8},
    {"code": "TH", "name": "Thailand", "region": "Asia", "lat": 15.0, "lon": 100.0},
    {"code": "TW", "name": "Taiwan", "region": "Asia", "lat": 23.5, "lon": 121.0},
    {"code": "VN", "name": "Vietnam", "region": "Asia", "lat": 16.0, "lon": 106.0},
]


def seed_location(conn: duckdb.DuckDBPyConnection) -> None:
    """Populate the silver.location table with country data.

    Args:
        conn: DuckDB connection.
    """
    for loc in _LOCATIONS:
        sql_insert = """
            INSERT OR REPLACE INTO silver.location (
            country_code, country_name, region, latitude, longitude)
            VALUES (?, ?, ?, ?, ?)
            """
        conn.execute(
            sql_insert,
            [loc["code"], loc["name"], loc["region"], loc["lat"], loc["lon"]],
        )
