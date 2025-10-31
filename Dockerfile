FROM python:3.12-slim AS base

ENV POETRY_VERSION=1.8.2 \
    POETRY_HOME=/opt/poetry \
    PATH="/opt/poetry/bin:$PATH"

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --without dev --no-root

COPY app ./app
COPY samples ./samples
COPY schemas ./schemas
COPY openapi ./openapi

RUN useradd --create-home --shell /bin/bash appuser
USER appuser

ENV PORT=8000
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD curl -fs http://localhost:8000/healthz || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
