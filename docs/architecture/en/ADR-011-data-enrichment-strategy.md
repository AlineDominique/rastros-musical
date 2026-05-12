# ADR-011: Data Enrichment Strategy for Propagation Analysis

**Status:** Accepted
**Date:** 2026-05-12

---

## Context

Phase 2 of the MVP was completed with 20 manually validated genres (Wikipedia) and Google Trends propagation data. However, Google Trends only has data from 2004 onwards, resulting in only 7 propagation records and a gap of more than 100 years between the origin of genres like Tango (1880) and its first recorded search in South Korea (2004).

To answer the project's core question — "How does a music genre spread across the world over time?" — it is necessary to fill this gap with propagation data prior to 2004.

After analyzing multiple sources (Musicmap, Google Music Timeline, Every Noise at Once, Radiooooo.com, Million Song Dataset), the **Million Song Dataset (MSD)** was identified as the only public database that provides year, country, and coordinates for a large volume of songs (1922–2011).

## Decision

Adopt three complementary sources for progressive data enrichment:

| Source | Role | Data type |
|--------|------|-----------|
| **Musicmap** | Curation: refine year and location of origin for the 20 genres | Visual genealogy (manual query) |
| **Every Noise at Once** | Validation: lists of representative artists per genre | Playlists and artists (manual query) |
| **Million Song Dataset** | Propagation: year, country, and coordinates for 1 million songs | Public dataset (download + processing) |

Implementation will occur in **Phase 2.5 (Data Enrichment)**, after completing the API (Phase 3).

## Alternatives considered

| Alternative | Pros | Cons |
|-------------|------|------|
| **Keep Google Trends only** | Already implemented | Insufficient data (only 7 records) |
| **Radiooooo.com** | API available, curated data | Private Ruby API, no official support |
| **Spotify Charts** | Current popularity | No historical data prior to 2015 |
| **Million Song Dataset** | 1922–2011 coverage, free | 280 GB (1.8 GB subset available), requires preprocessing |

## Consequences

**Positive:**
- Continuous temporal coverage from 1922 to 2011, filling the gap between historical origins and Google Trends
- Precise location data (country_code, latitude, longitude) for each track
- 1.8 GB subset (10,000 songs) viable for local processing

**Negative:**
- Requires download and preprocessing of HDF5 files
- Artist→genre association depends on MSD's own metadata (MusicBrainz tags)
- Additional manual curation to filter false positives
- Increases data pipeline complexity