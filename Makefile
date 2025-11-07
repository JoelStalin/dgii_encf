.PHONY: up down logs migrate test lint typecheck build requirements

COMPOSE_FILE ?= docker-compose.yml

up: ## Start local stack
	docker compose -f $(COMPOSE_FILE) up -d

down: ## Stop local stack
	docker compose -f $(COMPOSE_FILE) down --remove-orphans

logs: ## Tail application logs
	docker compose -f $(COMPOSE_FILE) logs -f web

migrate: ## Apply database migrations inside the web service
	docker compose -f $(COMPOSE_FILE) exec web alembic upgrade head

test: ## Run unit and integration tests
	poetry run pytest -q

lint: ## Run Ruff static analysis
	poetry run ruff check app tests

typecheck: ## Run mypy type checks
	poetry run mypy app

build: ## Build production image
	docker build -t dgii-ecf-web:latest -f Dockerfile .

requirements: ## Export locked dependencies for Docker builds
	poetry export --only main --without-hashes --format requirements.txt --output requirements.txt
