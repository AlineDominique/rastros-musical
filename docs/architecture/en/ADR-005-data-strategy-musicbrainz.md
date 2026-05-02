# ADR 005: Data Strategy with MusicBrainz

## Status
Accepted

## Context
The map's goal is to show geographical and temporal evolution. We need a source that provides historical metadata (start dates) and precise location (countries and cities) without relying on commercial popularity algorithms.

## Decision
We will use **MusicBrainz** as our **Single Source of Truth** for this MVP:
*   **Geographical Data:** We will use `area` and `coordinates` fields to feed the map.
*   **Temporal Data:** We will focus on the `begin-date` field to build the timeline.
*   **Data Engine:** **DuckDB** will ingest this data to allow fast aggregation queries by continent.

## Consequences
### Positive
*   **Integrity:** Historical data verified by the MusicBrainz community.
*   **Performance:** Local queries in DuckDB eliminate external API latency.
*   **Focus:** Removing Spotify API reduces authentication complexity and focuses on data engineering.

### Negative
*   **Data Volume:** MusicBrainz is vast and requires rigorous initial cleaning for the LatAm and Asia axes.