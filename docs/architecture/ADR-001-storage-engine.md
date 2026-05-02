# ADR 001: Selection of DuckDB as the Analytical Storage Engine

## Status
Accepted

## Context
The **Rastros Musical** project requires a robust engine to process and analyze music propagation data between Latin America and Asia. The data includes geographical coordinates, temporal series, and popularity metrics. 

We needed a solution that:
1. Supports high-performance analytical queries (OLAP).
2. Handles spatial/geographical data efficiently.
3. Is easy to set up in development and CI/CD environments without the overhead of a dedicated database server.
4. Integrates seamlessly with Python 3.13 and the modern data stack (Pandas/Polars).

## Decision
We have decided to use **DuckDB** as the primary analytical engine, along with its official **Spatial Extension**.

## Consulted Options
*   **PostgreSQL + PostGIS:** Robust but requires managing a separate database server/container, increasing infrastructure complexity for an initial stage.
*   **SQLite:** Easy to use, but lacks native high-performance analytical capabilities (columnar storage) and has limited spatial support compared to DuckDB.
*   **Pandas (In-memory):** Efficient for small scales but lacks SQL interface for complex relational joins and persistent spatial indexing.

## Consequences
### Positive
*   **Performance:** DuckDB's columnar engine is optimized for the types of aggregations we will perform (e.g., average popularity per region per year).
*   **Simplicity:** The database is stored in a single file, making it portable and easy to back up or version if necessary.
*   **Spatial Capabilities:** The Spatial extension allows us to perform "Points in Polygon" and distance calculations directly via SQL.
*   **Integration:** Direct compatibility with FastAPI and Pydantic through the Python API[cite: 1].

### Negative
*   **Concurrency:** DuckDB is optimized for single-writer workloads. This is acceptable for our ETL process but must be managed if we scale to multiple simultaneous data-writing services.
*   **Persistence:** As an in-process database, we must ensure Docker volumes are correctly configured to prevent data loss when containers are destroyed.

## References
* [DuckDB Documentation](https://duckdb.org/docs/)[cite: 1]
* [DuckDB Spatial Extension](https://duckdb.org/docs/extensions/spatial)[cite: 1]