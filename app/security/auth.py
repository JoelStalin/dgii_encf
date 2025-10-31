"""HTTP security helpers (CORS)."""
from __future__ import annotations

from typing import Iterable

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def setup_security(app: FastAPI, allowed_origins: Iterable[str]) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(allowed_origins),
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
        expose_headers=["X-Request-ID"],
    )
