DOCKER_EXEC = docker compose exec app

build:
	docker compose up --build

up:
	docker compose up
down:
	docker compose down

test:
	$(DOCKER_EXEC) pytest

lint:
	$(DOCKER_EXEC) ruff check . --fix

format:
	$(DOCKER_EXEC) ruff format .

check: lint test

test-cov:
	$(DOCKER_EXEC) pytest --cov=app tests/ --cov-report=term-missing