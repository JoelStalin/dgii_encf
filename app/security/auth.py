"""HTTP security helpers (CORS)."""
from __future__ import annotations

from typing import Iterable

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def setup_security(app: FastAPI, allowed_origins: Iterable[str]) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(allowed_origins),
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type", "X-Request-ID", "X-Trace-ID", "Accept"],
        expose_headers=["X-Request-ID"],
        allow_credentials=True,
        max_age=3600,
    )
