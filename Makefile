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