# ADR-010: Data sources for music propagation tracking

**Status:** Accepted
**Date:** 2026-05-07
**Deciders:** Aline Dominique

---

## Context

Phase 2 of the MVP used MusicBrainz exclusively as the data source. During ingestion, quality issues were identified:

- Imprecise collaborative tags (e.g., Coleman Hawkins tagged as samba)
- Artist birth dates instead of music production dates
- Geographic outliers (e.g., K-Pop in Lithuania)
- Inability to validate actual genre propagation

MusicBrainz is an artist database, not a genre propagation tracker.

## Decision

Replace MusicBrainz with three complementary sources:

| Source | Question answered | Data type |
|--------|-------------------|-----------|
| **Wikipedia** | Where and when did the genre emerge? | Manual curation |
| **Google Trends** | When did the genre start being searched in each country? | Time series |
| **Spotify Charts** | Where is the genre listened to today? | Popularity by country |

The MusicBrainzClient will be removed. The rest of the pipeline (Medallion, DuckDB, tests) remains intact.

## Alternatives considered

| Alternative | Pros | Cons |
|-------------|------|------|
| **Keep MusicBrainz** | Already implemented | Imprecise data, does not answer the project's question |
| **MusicBrainz + manual curation** | Reuses existing code | Curation does not solve the core issue (birth dates vs. production dates) |
| **Wikipedia + Google Trends + Spotify** | Accuracy, multiple dimensions | Requires implementing new clients |

## Consequences

**Positive:**
- Genre origins validated by human curation (Wikipedia)
- Measurable temporal propagation (Google Trends)
- Geolocated current popularity (Spotify Charts)
- Data directly answers the project's core question

**Negative:**
- Google Trends requires an external library (`pytrends`) with unofficial support
- Spotify requires an API token with renewal
- Manual origin table requires maintenance
- MusicBrainzClient and its tests will be removed

## Preserved structure

- Medallion Architecture (Bronze/Silver/Gold)
- DuckDB + Spatial Extension
- FastAPI
- Tests, CI/CD, logging
- Makefile, Docker