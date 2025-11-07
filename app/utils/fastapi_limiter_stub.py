"""Fallback stub for fastapi-limiter when dependency is unavailable."""
from __future__ import annotations

from typing import Any


class FastAPILimiter:
    redis = None

    @classmethod
    async def init(cls, redis_client: Any) -> None:
        cls.redis = redis_client

    @classmethod
    def close(cls) -> None:
        cls.redis = None


class RateLimiter:  # pragma: no cover - used only when fastapi-limiter missing
    def __init__(self, times: int, seconds: int) -> None:
        self.times = times
        self.seconds = seconds

    async def __call__(self, *args: Any, **kwargs: Any) -> None:  # noqa: D401 - mimic dependency signature
        return None
