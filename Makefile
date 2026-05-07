DOCKER_EXEC = docker compose exec app

build:
	docker compose up --build -d

up:
	docker compose up

down:
	docker compose down

test:
	$(DOCKER_EXEC) uv run pytest app/tests

lint:
	$(DOCKER_EXEC) uv run ruff check .

format:
	$(DOCKER_EXEC) uv run ruff format .
	$(DOCKER_EXEC) uv run ruff check --fix .

check: lint test

test-cov:
	$(DOCKER_EXEC) uv run pytest --cov=app app/tests/ --cov-report=term-missing

logs:
	docker compose logs -f app

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -rf htmlcov .coverage coverage.xml


# ===== Database Setup =====

DB_SETUP:
	$(DOCKER_EXEC) uv run python -c "from app.db.database import db_manager; from app.db.setup import setup_database; from app.db.seed_location import seed_location; with db_manager.get_connection() as conn: setup_database(conn); seed_location(conn); print('Database setup complete.')"

DB_SEED:
	$(DOCKER_EXEC) uv run python -c "from app.db.database import db_manager; from app.db.seed_location import seed_location; with db_manager.get_connection() as conn: seed_location(conn); print('Countries seeded.')"

INGEST:
	$(DOCKER_EXEC) uv run python -m app.run_ingestion


# ===== Database Diagnostics (read-only, safe) =====

DB_STATS:
	$(DOCKER_EXEC) uv run python -m app.db.diagnostics stats

DB_TOP_COUNTRIES:
	$(DOCKER_EXEC) uv run python -m app.db.diagnostics countries

DB_TOP_GENRES:
	$(DOCKER_EXEC) uv run python -m app.db.diagnostics genres

DB_SAMPLE_ARTISTS:
	$(DOCKER_EXEC) uv run python -m app.db.diagnostics sample