"""Minimal Redis asyncio stub used when redis-py is unavailable."""
from __future__ import annotations

from typing import Any


class Redis:  # pragma: no cover - compatibility stub
    def __init__(self, url: str = "redis://localhost:6379/0", **_: Any) -> None:
        self._url = url

    async def ping(self) -> bool:
        return True

    async def close(self) -> None:
        return None


def from_url(url: str, **kwargs: Any) -> Redis:
    return Redis(url=url, **kwargs)
