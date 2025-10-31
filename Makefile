.PHONY: setup lint typecheck test run docker-build docker-up

setup:
	poetry install --sync

lint:
	poetry run ruff check .

typecheck:
	poetry run mypy app/dgii

test:
	poetry run pytest

run:
	poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

docker-build:
	docker build -t dgii-ecf-api -f Dockerfile .

docker-up:
	docker compose up --build
