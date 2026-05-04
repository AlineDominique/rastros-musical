# ADR-009: Dependency management with `pyproject.toml` and `uv`

**Status:** Accepted  
**Date:** 2026-05-04  

---

## Context

The project used `requirements.txt` and `requirements-dev.txt` with `pip`. The Python ecosystem has consolidated `pyproject.toml` (PEP 621) as the standard and `uv` as a fast, deterministic package manager.

## Decision

Replace `requirements.txt` with dependencies declared in `pyproject.toml` and adopt `uv` as the package manager. The `uv.lock` file ensures reproducible builds.

## Alternatives considered

| Alternative | Speed | Lock file | PEP 621 | Ruff integration | Learning curve |
|-------------|:----------:|:---------:|:-------:|:---------------:|:-----:|
| `pip` + `pip-tools` | Slow | ✅ | ❌ | ❌ | Low |
| Poetry | Medium | ✅ | ❌ | ❌ | Medium |
| PDM | Medium | ✅ | ✅ | ❌ | Medium |
| **uv** | **Very fast** | ✅ | ✅ | ✅ | Low |

## Consequences

**Positive:**
- Single file: `pyproject.toml` replaces multiple dependency files
- `uv.lock` ensures idempotent builds across all environments
- Up to 10x faster installation than `pip` in Docker and CI

**Negative:**
- `uv` must be available in the environment (local or Docker)
- Hatchling requires `[tool.hatch.build.targets.wheel]` and validates `readme`

## Problems solved during migration

1. **Lock file without `uv` local** — Used the old Docker container (pip-based) to install `uv` and generate `uv.lock` via mounted volume
2. **Missing README during build** — Added `COPY README.md` before `uv sync` in Dockerfile
3. **No build target defined** — Added `packages = ["app"]` in `[tool.hatch.build.targets.wheel]`