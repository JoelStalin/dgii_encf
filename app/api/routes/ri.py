"""Placeholder for RI rendering."""
from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/render")
async def render_ri() -> dict[str, str]:
    return {"detail": "RI rendering pending"}
