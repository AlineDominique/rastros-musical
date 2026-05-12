# Rastros Musical 🎵


![Python: 3.13](https://img.shields.io/badge/Python-3.13-blue?style=flat-square)
![Database: DuckDB](https://img.shields.io/badge/Database-DuckDB-fff100?style=flat-square&logo=duckdb&logoColor=black)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat-square&logo=fastapi)

![CI Pipeline](https://github.com/AlineDominique/rastros-musical-api/actions/workflows/ci.yml/badge.svg)
![Linter: Ruff](https://img.shields.io/badge/Linter-Ruff-4b7aed?style=flat-square)
![Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/AlineDominique/66c52db472148abeda19137803004a81/raw/coverage.json)

**Rastros Musical** is a data engineering and visualization platform designed to track the spread and evolution of musical genres between **Latin America** and **Asia**.

[Portuguese (BR) Version](./docs/architecture/pt/README-PT.md)

---

## 🌍 Internationalization (i18n)
The project is built to be multilingual, natively supporting:
*   **Português** (BR)
*   **English** (US)
*   **Español** (ES)

## 🏗️ Tech Stack

### Backend & Data Engineering
*   **Language:** [Python 3.13](https://docs.python.org/3.13/) (Focus on Type Hinting & [Pydantic](https://docs.pydantic.dev/))
*   **API Framework:** [FastAPI](https://fastapi.tiangolo.com/)
*   **Data Engine:** [DuckDB](https://duckdb.org/) (In-process OLAP database)
*   **Spatial Support:** [DuckDB Spatial Extension](https://duckdb.org/docs/extensions/spatial)
*   **Quality Assurance:** [Pytest](https://docs.pytest.org/) & [Ruff](https://docs.astral.sh/ruff/) (Linter & Formatter)

### Frontend & Visualization
*   **Framework:** [React](https://react.dev/) (UI & State Management)
*   **Visualization:** [Deck.gl](https://deck.gl/) (Large-scale WebGL-powered Data Visualization)
*   **Internationalization:** [i18next](https://www.i18next.com/) (Support for PT/EN/ES)

### Infrastructure & Automation
*   **Containerization:** [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)
*   **CI/CD:** [GitHub Actions](https://github.com/features/actions)
*   **Automation:** [GNU Make](https://www.gnu.org/software/make/)

## 📂 Project Structure
```text
rastros_musical/
├── .github/workflows/  # CI/CD Pipelines (GitHub Actions)
├── app/                # Backend Core (Python & FastAPI)
│   ├── api/            # FastAPI Endpoints & API Logic
│   ├── core/           # Business Logic, Projections & Services
│   ├── db/             # Data Access Layer & DuckDB Integration
│   ├── schemas/        # Data Contracts & Validation (Pydantic)
│   └── tests/          # Backend Unit & Integration Tests
├── web/                # Frontend (React & Deck.gl) [Planned]
├── data/               # Persistent Storage (Medallion Architecture)
│   ├── raw/            # Bronze Layer: Immutable Raw Data
│   └── processed/      # Silver/Gold Layers: Cleaned & Analytical Data
├── docs/               # Technical Documentation
│   └── architecture/   # Architecture Decision Records (ADRs)
│   └── management/     # Project MAnagement (TODOS)
├── Makefile            # Project Automation Commands
├── pyproject.toml      # Build System, Ruff & Pytest Configuration
├── docker-compose.yml  # Multi-container Orchestration
└── Dockerfile          # Backend Container Definition
```


## 🚀 Getting Started

### Prerequisites
*   Docker & Docker Compose
*   Make (optional, but recommended)

1. **Clone the repository and Access the folder:**

    ```bash 
    git clone https://github.com/AlineDominique/rastros-musical-api
    cd rastros_musical
    ```

### Development Workflow
We use a `Makefile` to standardize common operations. If you don't have `make` installed, you can run the commands inside the brackets directly in your terminal.

1.  **Build the environment:**
    ```bash
    make build  # [docker-compose up --build]
    ```

2.  **Run the application:**
    ```bash
    make up     # [docker-compose up]
    ```

3.  **Run Tests:**
    ```bash
    make test   # [docker-compose exec app pytest]
    ```

4.  **Lint & Format Code:**
    ```bash
    make lint    # [docker-compose exec app ruff check . --fix]
    make format  # [docker-compose exec app ruff format .]
    ```

### Managing Dependencies

This project uses [uv](https://docs.astral.sh/uv/) and `pyproject.toml` (PEP 621) for dependency management. Production dependencies are declared in `[project.dependencies]` and development dependencies in `[project.optional-dependencies] dev`. The lock file `uv.lock` ensures reproducible builds.

1. **Adding a new dependency:**
    ```bash
        # Production dependency
        uv add httpx

        # Development dependency
        uv add --dev pytest-watch
    ```
2. **Updating all dependencies:**
    ```bash
        uv lock --upgrade
    ```
3. **Syncing the environment (inside the container):**
    ```bash
    docker compose exec app uv sync --dev
    ```

## Documentation
For detailed information on technical decisions and architectural justifications, please refer to our Architecture Decision Records **(ADRs)** located in `docs/architecture/en/`.

## Project Management

The strategic planning and task tracking for this project are centralized in our management documentation. We follow a phased approach to ensure the non-negotiable data precision required for this ecosystem.

You can follow our live progress here:
**[Full Development Roadmap](./docs/management/todo-en.md)**

### Current Status:
- **Phase 1 (Foundation):** Completed ✅
- **Phase 2 (Data Engineering):** Completed ✅
- **Phase 3 (Service API):** Completed ✅