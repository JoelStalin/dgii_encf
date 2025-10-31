# dgii_encf — Plataforma DGII e-CF endurecida

Backend FastAPI (Python 3.12) con controles de seguridad y cumplimiento para integraciones DGII e-CF.

## Características clave

- Parser XML seguro (`defusedxml`), límites de tamaño/profundidad, validación XSD previa a firma/envío.
- Firma XMLDSig RSA-SHA256 (enveloped, referencia vacía, C14N) con certificados `.p12` externos.
- Cliente HTTP con allow-list, anti-SSRF, timeouts estrictos, retries con backoff y circuit breaker.
- Rate limiting por IP, CORS explícito, cabeceras de seguridad y logging JSON (`structlog`).
- Docker multi-stage (distroless) y Nginx con cabeceras endurecidas.
- CI: lint (`ruff`), mypy, pytest, análisis de dependencias (`pip-audit`) y escaneo de imagen (`trivy`).

## Variables de entorno principales

| Variable | Descripción |
| --- | --- |
| `DGII_ENV` | Ambiente DGII (`PRECERT`, `CERT`, `PROD`). |
| `DGII_ALLOWED_HOSTS` | Hosts DGII permitidos (lista separada por comas). |
| `DGII_TOKEN_URL`, `DGII_SUBMISSION_URL`, `DGII_STATUS_URL` | Endpoints oficiales DGII. |
| `DGII_P12_PATH`, `DGII_P12_PASSWORD` | Ruta y contraseña del certificado `.p12` (mantener fuera del repo). |
| `CORS_ALLOW_ORIGINS` | Orígenes permitidos para CORS. |
| `RATE_LIMIT_PER_MINUTE` | Solicitudes permitidas por IP/minuto. |
| `POSTGRES_DSN` | Cadena de conexión a PostgreSQL 18. |
| `JWT_SECRET` | Secreto para firmar JWT de corta duración. |

## Puesta en marcha

```bash
cp .env.example .env
poetry install
poetry run alembic upgrade head
poetry run uvicorn app.main:app --reload
```

## Pruebas

```bash
poetry run pytest
```

## Despliegue con Docker

```bash
docker compose up --build
```

`docker/nginx.conf` aplica cabeceras seguras. Sustituye los valores en `.env`/secrets antes de producción.
