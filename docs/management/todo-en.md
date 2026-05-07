# 🚀 Full-Stack Development Roadmap: Rastros Musical

This document tracks the MVP progress, integrating data engineering, backend services, and geographic visualization within a Monorepo structure.

---

## 🟢 Phase 1: Foundation & Infrastructure (Docker & Docs)

### ✅ Completed
- [X] **Governance Documentation**: Review and update ADRs for the Monorepo structure.
- [X] **Directory Structure**: Create `/app` (Backend), `/web` (Frontend), `/data`, and `/docs` folders.
- [X] **Docker Setup**: Create Dockerfile for Backend and docker-compose.yml for orchestration (Python 3.13).
- [X] **Quality Setup**: Configure Ruff, Pytest, and Coverage with omission rules in pyproject.toml.
- [X] **CI/CD Pipeline**: Set up GitHub Actions to run the make check pipeline.

---

## 🔵 Phase 2: Data Engineering (Medallion Architecture)

### ✅ Completed
- [X] **Pydantic Schemas**: Define data contracts for Artists, Genres, and Locations.
- [X] **Data Setup**: Configure DuckDB spatial extensions for geographic support.

### 🎯 MVP (Multi-Source Data)
- [ ] **Wikipedia (Origin)**: Manual table with country and year of emergence for each genre.
- [ ] **Google Trends (Propagation)**: Client to fetch first significant search by country.
- [ ] **Spotify Charts (Popularity)**: Client to get current popularity by country.
- [ ] **Silver Layer (Normalization)**: Integrate and clean data from all three sources.
- [ ] **Essential Gold Layer**: Create `gold.genre_first_appearance` with consolidated data.

### 📈 Future Increments
- [ ] **Ingestion automation**: Periodic updates via GitHub Actions.
- [ ] **Cross-validation**: Compare data from all three sources for consistency.
- [ ] **Silver Layer (Normalization)**: `country_code` validation against ISO 3166-1, name normalization (strip, title case), and artist deduplication by name and country.
- [ ] **Gold Layer (Advanced)**: Analytical tables for growth (`gold.genre_growth`), comparative popularity, and temporal aggregations.

---

## 🟡 Phase 3: Service API (FastAPI)

### 🎯 MVP (Two Essential Endpoints)
- [ ] **Database Singleton**: Manage persistent connections to the `.db` file.
- [ ] **Genres Endpoint**: `GET /api/genres` returning the list of unique available genres.
- [ ] **Propagation Endpoint**: `GET /api/propagation?genre=...&year=...` returning countries where the genre appeared up to the given year (lat, lon, year).
- [ ] **OpenAPI Documentation**: Write clear Swagger examples for easy frontend consumption.

### 📈 Future Increments
- [ ] **Time-Series Endpoints**: Routes for detailed evolution (releases per year/country) and migration metrics.
- [ ] **Data Audit**: Health check that validates table consistency before deployment.

---

## 🟠 Phase 4: Interface & Visualization (React + Deck.gl)

### 🎯 MVP (Live Map with Minimal Controls)
- [ ] **Framework Setup (/web)**: Initialize React project (Vite) without initial i18n.
- [ ] **ScatterplotLayer Map**: Display colored dots representing the first appearance of a genre in each country.
- [ ] **Genre Dropdown**: Select a genre from the list obtained via the API.
- [ ] **Time-Slider Component**: Slider (1970–2026) that triggers new API calls on change.
- [ ] **Simple Tooltip**: Show country and year on hover.

### 📈 Future Increments
- [ ] **i18n Setup**: Add PT/EN/ES support to UI components.
- [ ] **ArcLayer / IconLayer Integration**: Show origin/destination flows when source country data is available.
- [ ] **Metrics Dashboard**: Comparative charts (e.g., regional popularity) below the map.
- [ ] **Multiple Genres**: Allow selecting more than one genre for visual comparison.

---

## 🔴 Phase 5: DevOps & Automated Deploy (Free)

### 🎯 MVP (Manual Deploy with Public Link)
- [ ] **Backend Deploy**: Deploy `/app` container to Fly.io.
- [ ] **Frontend Deploy**: Build and deploy `/web` to Vercel.
- [ ] **Environment Variables**: Configure API URL in the frontend to point to Fly.io.

### 📈 Future Increments
- [ ] **Automated Backend Deploy**: Full CI/CD linking the repo to Fly.io via GitHub Actions.
- [ ] **Automated Frontend Deploy**: Full CI/CD linking the repo to Vercel via GitHub Actions.
- [ ] **Final Data Audit**: Proactive consistency check executed in the pipeline before each deploy.