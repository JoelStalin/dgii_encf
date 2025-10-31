# GetUpNet — Plataforma DGII e-CF

GetUpNet es una referencia arquitectónica basada en FastAPI para la emisión y recepción de comprobantes fiscales electrónicos (e-CF) de la DGII República Dominicana. Está preparada para escenarios multi-tenant, integra mecanismos de seguridad alineados a ISO/IEC 25010, PCI DSS 4.0 y OWASP 2025, e incluye flujos de integración con Odoo 18.

## Características destacadas

- Microservicios de autenticación, firmado, integración DGII, recepción sandbox, facturación y representación impresa.
- Cliente DGII resiliente con firma XMLDSig SHA-256, validación XSD y colas internas de reintentos.
- Representación Impresa con plantillas Jinja2, generación de QR y exportación HTML/PDF.
- Modelado de datos en PostgreSQL mediante SQLAlchemy 2 y migraciones Alembic.
- Seguridad con almacenamiento WORM, auditoría con hash encadenado y trazabilidad distribuida.
- Observabilidad con Prometheus/Grafana/Loki y despliegue con Nginx (TLS 1.3).
- Suite de pruebas Pytest con cobertura ≥ 85%, linters (ruff) y type-checking (mypy).

## DGII e-CF (Cumplimiento)

- **OpenAPI 3.1** (`openapi/dgii.yaml`) sincronizado con los routers `/api/dgii/*` y `/ri/*`.
- **Clientes DGII** (`DGIIClient`) con flujos `semilla → token → envíos`, reintentos exponenciales e idempotencia.
- **Panel administrativo** para analizar contabilidad de e-CF y parametrizar compañías (asientos, totales, configuración contable).
- **Validación técnica**: XSD en `schemas/`, firma RSA-SHA256 (`app/dgii/signing.py`) y pruebas contractuales con `respx`.
- **Representación Impresa**: endpoint `/ri/render` con QR dinámico, validaciones de longitud y PDF generado con ReportLab.
- **DevOps listo**: `Dockerfile`, `docker-compose.yaml`, `Makefile` (`make lint|typecheck|test|run`) y workflow CI (`.github/workflows/ci.yml`).
- **Documentación**: `docs/DGII-Guia-Implementacion.md` y `docs/SEGURIDAD-PROVEEDOR.md` cubren setup, certificación y seguridad.

## Requisitos previos

- `Python 3.12`
- `Poetry 1.8+`
- `Docker` y `docker compose` (opcionales para despliegues locales con contenedores)
- Acceso a un motor PostgreSQL para entornos no SQLite

## Instalación rápida

1. Clona el repositorio y ubícate en la raíz del proyecto:
   ```bash
   git clone <url-del-repositorio>
   cd dgii_encf
   ```
2. Asegura permisos de ejecución para el instalador:
   ```bash
   chmod +x scripts/install.sh
   ```
3. Ejecuta el instalador interactivo:
   ```bash
   ./scripts/install.sh
   ```

El instalador verifica dependencias del sistema, crea `.env.development` a partir de `.env.example` si aún no existe e instala las dependencias del proyecto con Poetry. Revisa el archivo generado y actualiza las credenciales sensibles antes de levantar servicios conectados a terceros.

## Configuración del entorno

- Variables de entorno: ajusta `.env.development` con credenciales DGII, claves de firmado y parámetros de base de datos. Usa `scripts/setup_env.py` para regenerar el archivo si es necesario.
- Migraciones: en entornos PostgreSQL ejecuta `poetry run alembic upgrade head` una vez configurado `DATABASE_URL`.
- Seeds: la carpeta `docs/guide/` incluye ejemplos de flujos e2e para poblar datos de prueba.

## Puesta en marcha (desarrollo)

Levanta la API con recarga automática:

```bash
poetry run uvicorn app.main:app --reload
```

La documentación interactiva estará disponible en `http://127.0.0.1:8000/docs` y el expediente de trazabilidad en `http://127.0.0.1:8000/redoc`. Los endpoints `/healthz`, `/readyz` y `/metrics` permiten integrar chequeos de infraestructura.

## Despliegue automatizado con Docker Compose

Para levantar la plataforma con la pila de contenedores incluida:

```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

El script valida `.env.development`, construye las imágenes, ejecuta las migraciones de Alembic y expone la API en `https://localhost:8443` detrás de Nginx con certificados auto-firmados para pruebas. Ajusta variables como `DOMAIN`, `SSL_CERT_PATH` y `SSL_KEY_PATH` antes de desplegar en entornos productivos.

## Estructura principal del proyecto

- `app/`: servicios de autenticación, facturación, integración DGII, firmado y representación impresa.
- `app/shared/`: configuración, base de datos y utilidades comunes (logging, tracing, seguridad).
- `alembic/`: migraciones de base de datos y plantillas.
- `frontend/`: shell inicial para panel administrativo o integración con Odoo.
- `infra/`: definiciones de infraestructura como código para entornos cloud.
- `scripts/`: automatizaciones de setup, despliegue y utilidades operativas.
- `docs/guide/`: guías de implementación, cumplimiento y arquitectura.

## Pruebas y verificación

Ejecuta la suite de tests:

```bash
poetry run pytest
```

Atajos disponibles mediante `Makefile`:

```bash
make lint      # ruff
make typecheck # mypy app/dgii
make test      # pytest con cobertura
```

Para ejecutar pruebas end-to-end contra la sandbox DGII, configura las credenciales y certificados requeridos en el `.env.development`.

## Documentación adicional

- `docs/guide/15-implementacion-aws.md`: paso a paso para desplegar en AWS.
- `docs/guide/16-arquitectura-eks.md`: topología recomendada e integración con EKS.
- `docs/guide/`: guías de operación, seguridad y cumplimiento DGII.
