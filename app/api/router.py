"""Root API router."""
from __future__ import annotations

from fastapi import APIRouter

from app.api.routes import auth, dgii, ri, receptor

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(dgii.router, prefix="/dgii", tags=["dgii"])
api_router.include_router(ri.router, prefix="/ri", tags=["ri"])
api_router.include_router(receptor.router, prefix="/receptor", tags=["receptor"])
