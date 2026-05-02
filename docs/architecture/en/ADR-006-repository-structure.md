# ADR 005: Repository Structure (Monorepo)

## Status
Proposed

## Context
**Rastros Musical** consists of an analytical data API and a visualization interface. We need to decide whether to separate these components into distinct repositories or keep them together.

## Decision
We will adopt the **Monorepo** strategy. Backend code will reside in `/app` and Frontend in `/web`.

## Rationale
1. **Contract Sync**: Ensures that changes in data Schemas (Pydantic) and the interface happen simultaneously.
2. **Deployment Simplicity**: Facilitates the configuration of free CI/CD (Vercel/Render) in a single workflow.
3. **Strategic Vision**: Centralizes governance (ADRs, TODO.md) and the data lifecycle evolution history.

## Consequences
* **Positive**: Easier cross-stack refactoring and single issue management.
* **Negative**: Repository size grows faster, but it is irrelevant for an MVP scale.