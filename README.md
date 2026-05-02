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
*   **Language:** [Python 3.13](https://docs.python.org/3.13/) (Focus on Type Hinting & [Pydantic](https://docs.pydantic.dev/))
*   **API Framework:** [FastAPI](https://fastapi.tiangolo.com/)[cite: 1]
*   **Data Engine:** [DuckDB](https://duckdb.org/) (In-process OLAP database)
*   **Spatial Support:** [DuckDB Spatial Extension](https://duckdb.org/docs/extensions/spatial)[cite: 1]
*   **Quality Assurance:** [Pytest](https://docs.pytest.org/) (Testing) & [Ruff](https://docs.astral.sh/ruff/) (Linter & Formatter)
*   **Infrastructure:** [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)[cite: 1]
*   **CI/CD:** [GitHub Actions](https://github.com/features/actions)[cite: 1]
*   **Automation:** [GNU Make](https://www.gnu.org/software/make/)

## 📂 Project Structure
```text
rastros_musical/
├── .github/workflows/  # CI/CD Pipelines
├── app/                # Application Core
│   ├── api/            # FastAPI Endpoints
│   ├── core/           # Business Logic & Projections
│   ├── db/             # Data Layer (DuckDB)
│   └── schemas/        # Data Contracts (Pydantic)
├── data/               # Partitioned Storage
│   ├── raw/            # Immutable Raw Data
│   └── processed/      # Cleaned and Transformed Data
├── docs/               # Technical Documentation
│   └── architecture/   # Architecture Decision Records (ADRs)
├── docker-compose.yml  
└── Dockerfile
```


## 🚀 Getting Started

### Prerequisites
*   Docker & Docker Compose
*   Make (optional, but recommended)

1. **Clone the repository:**

```bash git clone https://github.com/seu-usuario/rastros_musical.git```

2. **Access the folder**

```bash cd rastros_musical```

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


## Documentation
For detailed information on technical decisions and architectural justifications, please refer to our Architecture Decision Records (ADRs) located in docs/architecture/.


