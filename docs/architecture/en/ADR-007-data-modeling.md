# ADR 006: Data Modeling and Flow

## Status
Proposed

## Context
The system must transform raw MusicBrainz metadata into insights about musical propagation between Latin America and Asia.

## Decision
We will use a layered architecture (Medallion) within **DuckDB**:
1. **Bronze (Raw)**: Direct ingestion from API/Dump.
2. **Silver (Trusted)**: Cleaned, typed data with geographical normalization.
3. **Gold (Refined)**: Temporal aggregations ready for the API.

## Flow Diagram


## Rationale
This approach ensures that **data precision is non-negotiable** and allows for auditing at each step of the analytical processing.

## Consequences
* **Positive**: Clear separation between extraction and business logic.
* **Negative**: Requires more disk storage to maintain intermediate layers.