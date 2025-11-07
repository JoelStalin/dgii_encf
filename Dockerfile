FROM python:3.12-slim AS build

ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libxml2-dev \
    libxslt1-dev \
    && rm -rf /var/lib/apt/lists/*
RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app
COPY pyproject.toml poetry.lock* ./
RUN poetry export --only main --format requirements.txt --output requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

FROM gcr.io/distroless/python3-debian12

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/usr/local/bin:/usr/bin:/bin"

WORKDIR /app
COPY --from=build /usr/local /usr/local
COPY --from=build /app /app

EXPOSE 8080
CMD ["-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
