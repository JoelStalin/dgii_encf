"""Punto de entrada FastAPI para GetUpNet."""
from __future__ import annotations

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.auth.routes import router as auth_router
from app.billing.routes import router as billing_router
from app.dgii.routes import router as dgii_router
from app.receiver.routes import router as receiver_router
from app.ri.routes import router as ri_router
from app.shared.settings import settings
from app.shared.tracing import ensure_trace_id
from app.sign.routes import router as sign_router

app = FastAPI(title=settings.app_name, version="1.0.0")


@app.middleware("http")
async def add_tracing_headers(request: Request, call_next):  # type: ignore[override]
    """Inserta encabezados de trazabilidad en todas las respuestas."""

    trace_id = ensure_trace_id(request)
    response = await call_next(request)
    response.headers.setdefault(settings.tracing_header, trace_id)
    request_id = request.headers.get(settings.request_id_header)
    if request_id:
        response.headers.setdefault(settings.request_id_header, request_id)
    return response


if settings.cors_allow_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/healthz", tags=["Infra"])
async def healthz() -> dict[str, str]:
    """Endpoint de liveness."""

    return {"status": "ok"}


@app.get("/readyz", tags=["Infra"])
async def readyz() -> dict[str, str]:
    """Endpoint de readiness básico."""

    return {"status": "ready"}


@app.get("/metrics", tags=["Infra"])
async def metrics() -> JSONResponse:
    """Expone métricas básicas hasta integrar Prometheus."""

    payload = {"app": settings.app_name, "environment": settings.environment}
    return JSONResponse(payload)


app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(sign_router, prefix="/api", tags=["Firmado"])
app.include_router(dgii_router, prefix="/api", tags=["DGII"])
app.include_router(receiver_router, prefix="/api", tags=["Recepcion"])
app.include_router(billing_router, prefix="/api", tags=["Facturacion"])
app.include_router(ri_router, prefix="/api", tags=["RI"])
