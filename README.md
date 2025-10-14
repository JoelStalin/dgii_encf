# GetUpNet — Plataforma DGII e-CF

GetUpNet es una referencia arquitectónica basada en FastAPI para la emisión y recepción de comprobantes fiscales electrónicos (e-CF) de la DGII República Dominicana. El proyecto es multi-tenant, seguro y preparado para integraciones con Odoo 18.

## Características destacadas

- Microservicios de autenticación, firmado, integración DGII, recepción sandbox, facturación y representación impresa.
- Modelado de datos en PostgreSQL mediante SQLAlchemy 2 y migraciones Alembic.
- Seguridad de acuerdo con ISO/IEC 25010, PCI DSS 4.0 y OWASP 2025.
- Almacenamiento WORM, auditoría con hash encadenado y trazabilidad distribuida.
- Contenedores Docker, despliegue con Nginx (TLS 1.3) y observabilidad (Prometheus/Grafana/Loki).
- Suite de pruebas con Pytest (unitarias y flujo e2e básico).

## Cómo iniciar

```bash
git clone https://example.com/getupnet.git
cd getupnet
python scripts/setup_env.py
poetry install
uvicorn app.main:app --reload
```

## Despliegue automatizado con Docker Compose

Para levantar la plataforma con la pila de contenedores incluida:

```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

El script verifica la existencia de `.env.development`, construye las imágenes, ejecuta las migraciones de Alembic y deja la API expuesta en `https://localhost:8443` detrás de Nginx.

Consulta la guía completa en `docs/guide/` para detalles de operación, seguridad y cumplimiento DGII, incluyendo el paso a paso de despliegue en AWS descrito en `docs/guide/15-implementacion-aws.md`.
