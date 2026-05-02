# 🚀 Full-Stack Development Roadmap: Musical Traces

This document tracks the MVP progress, integrating data engineering, backend services, and geographic visualization within a Monorepo structure.

## 🟢 Phase 1: Foundation & Infrastructure (Docker & Docs) ✅
- [x] **Governance Documentation**: Review and update ADRs for the Monorepo structure (ADRs 005, 006, 008).
- [x] **Directory Architecture**: Initialize `/app` (Backend), `/data` (Storage), and `/docs` folders.
- [x] **Docker Environment**: Create `Dockerfile` (Python 3.13-slim) and `docker-compose.yml` for service orchestration.
- [x] **Quality Assurance Setup**: Configure Ruff (lint/format), Pytest, and Coverage with strict omission rules in `pyproject.toml`.
- [x] **CI/CD Pipeline**: Implement GitHub Actions workflow to automate `make check` on every push.

## 🔵 Phase 2: Data Engineering (Medallion Architecture) 🏗️
- [ ] **Pydantic Schemas**: Define data contracts for Artists, Genres, and Locations using Python 3.13 Type Hinting.
- [ ] **Bronze Layer (Raw)**: Implement MusicBrainz ingestion scripts for raw data storage.
- [ ] **Silver Layer (Trusted)**: Develop normalization logic and LatAm vs. Asia geographic mapping.
- [ ] **Gold Layer (Refined)**: Create aggregated analytical tables in DuckDB to power the API.
- [ ] **Spatial Data Setup**: Enable DuckDB spatial extensions for geographic coordinate support.

## 🟡 Phase 3: Service API (FastAPI)
- [ ] **Time-Series Endpoints**: Build routes for genre evolution and musical migration trends.
- [ ] **Database Singleton**: Manage persistent connections to the `.duckdb` file.
- [ ] **OpenAPI Documentation**: Validate schemas and provide Swagger examples for Frontend consumption.

## 🟠 Phase 4: Interface & Visualization (React + Deck.gl)
- [ ] **Setup do Framework (/web)**: Initialize React project with i18n support (PT/EN/ES) via Docker.
- [ ] **Deck.gl Integration**: Configure `ArcLayer` and `IconLayer` for dynamic geographic data rendering.
- [ ] **Time-Slider Component**: Develop UI controls for historical timeline navigation (1970 - 2026).
- [ ] **Metrics Dashboard**: Create comparison charts for regional popularity and influence.

## 🔴 Phase 5: DevOps & Deployment
- [ ] **Automated Backend Deploy**: Connect `/app` to Render or Koyeb.
- [ ] **Automated Frontend Deploy**: Connect `/web` to Vercel or Netlify.
- [ ] **Data Integrity Audit**: Implement proactive consistency checks before final deployment.