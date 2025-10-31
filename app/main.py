"""FastAPI application entrypoint."""
from __future__ import annotations

from fastapi import FastAPI, Request, Response

from app.api.router import api_router
from app.infra.logging import configure_logging
from app.infra.settings import settings
from app.security.auth import setup_security
from app.security.rate_limit import attach_rate_limiter


def create_app() -> FastAPI:
    configure_logging()
    app = FastAPI(title=settings.app_name, version="2.0.0")

    setup_security(app, allowed_origins=settings.cors_allow_origins)
    attach_rate_limiter(app, rate_limit_per_minute=settings.rate_limit_per_minute)

    app.include_router(api_router, prefix="/api")

    @app.middleware("http")
    async def security_headers(request: Request, call_next) -> Response:  # type: ignore[override]
        response = await call_next(request)
        response.headers.setdefault("Content-Security-Policy", "default-src 'self'")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("Referrer-Policy", "no-referrer")
        return response

    @app.get("/healthz", tags=["infra"])
    async def healthz() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/readyz", tags=["infra"])
    async def readyz() -> dict[str, str]:
        return {"status": "ready"}

    @app.get("/metrics", tags=["infra"])
    async def metrics() -> dict[str, str]:
        return {"app": settings.app_name, "env": settings.environment}

    return app


app = create_app()
