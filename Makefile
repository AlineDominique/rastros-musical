DOCKER_EXEC = docker compose exec app

build:
	docker compose up --build -d

up:
	docker compose up

down:
	docker compose down


test:
	$(DOCKER_EXEC) pytest app/tests

lint:
	$(DOCKER_EXEC) ruff check

format:
	$(DOCKER_EXEC) ruff format .
	$(DOCKER_EXEC) ruff check --unsafe-fixes .

check: lint test

test-cov:
	$(DOCKER_EXEC) pytest --cov=app app/tests/ --cov-report=term-missing