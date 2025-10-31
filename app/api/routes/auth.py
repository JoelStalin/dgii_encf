"""Authentication endpoints (placeholder)."""
from __future__ import annotations

from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException

from app.infra.settings import settings

router = APIRouter()


@router.post("/token")
def issue_token() -> dict[str, str]:
    """Issue a short-lived access token (stub)."""

    if not settings.jwt_secret:
        raise HTTPException(status_code=500, detail="JWT secret not configured")
    now = datetime.utcnow()
    expiry = now + timedelta(minutes=settings.jwt_access_exp_minutes)
    return {"access_token": "stub-token", "expires_at": expiry.isoformat() + "Z"}
