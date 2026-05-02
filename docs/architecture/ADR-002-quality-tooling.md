# ADR 002: Selection of Ruff for Linting and Formatting

## Status
Accepted

## Context
To ensure high code quality and consistency in the **Rastros Musical** project, we needed a toolset for linting (static analysis) and formatting. Traditionally, the Python ecosystem uses a combination of several tools like Flake8, Black, isort, and bandit. 

However, managing multiple tools increases:
1. Configuration complexity (multiple files like `.flake8`, `pyproject.toml`, etc.).
2. CI/CD execution time.
3. Potential conflicts between the formatter and the linter.

## Decision
We have decided to use **Ruff** as the unified tool for both linting and formatting.

## Consulted Options
*   **Black + Flake8 + isort:** The traditional industry standard. Very reliable but slow and requires managing three separate tool configurations.
*   **Pylint:** Extremely thorough but significantly slower and often produces a high volume of false positives that require manual suppression.
*   **Ruff:** A modern, extremely fast (written in Rust) linter and formatter that replaces Flake8, isort, Black, and dozens of other plugins.

## Consequences
### Positive
*   **Speed:** Ruff is 10x to 100x faster than traditional tools, providing near-instant feedback during development and reducing CI/CD costs[cite: 1].
*   **Unified Configuration:** All rules (linting, import sorting, formatting) are managed in a single `pyproject.toml` file[cite: 1].
*   **Built-in Fixes:** Ruff can automatically fix many common errors (like unused imports), which speeds up development[cite: 1].
*   **Modern Standards:** It natively supports the latest Python 3.13 features and best practices[cite: 1].

### Negative
*   **Ecosystem Maturity:** While very popular and stable, it is newer than Black or Flake8. However, it is already adopted by major projects like FastAPI, Pandas, and SciPy[cite: 1].

### Documentation Standards
*   **Language:** All code comments, docstrings, and commit messages must be in **English**.
*   **Format:** We follow the **Google Python Style Guide** for docstrings.
*   **Enforcement:** Ruff (pydocstyle) is configured to validate docstring presence and formatting.

## References
* [Ruff Documentation](https://docs.astral.sh/ruff/)
* [FastAPI's transition to Ruff](https://github.com/fastapi/fastapi/pull/10313)