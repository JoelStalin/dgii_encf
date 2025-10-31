"""Rate limiting setup."""
from __future__ import annotations

from fastapi import FastAPI
from slowapi import Limiter
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address


def attach_rate_limiter(app: FastAPI, rate_limit_per_minute: int) -> None:
    limiter = Limiter(key_func=get_remote_address, default_limits=[f"{rate_limit_per_minute}/minute"])
    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)
