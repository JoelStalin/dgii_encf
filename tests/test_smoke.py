"""Smoke tests for platform health endpoints."""
from __future__ import annotations

import pytest
from httpx import AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_livez_endpoint() -> None:
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/livez")
    assert response.status_code == 200
    assert response.json()["status"] == "alive"


@pytest.mark.asyncio
async def test_metrics_endpoint_exposes_prometheus_format() -> None:
    async with AsyncClient(app=app, base_url="http://test") as client:
        await client.get("/livez")
        response = await client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text
