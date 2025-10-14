"""Rutas de autenticación."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from app.auth.deps import get_service
from app.auth.schemas import LoginRequest, LoginResponse, MFARequest, UserRead
from app.auth.service import AuthService

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
async def login(payload: LoginRequest, service: AuthService = Depends(get_service)) -> LoginResponse:
    """Realiza autenticación tradicional (primer factor)."""

    _, tokens = service.authenticate(payload.email, payload.password)
    return tokens


@router.post("/mfa/verify", response_model=dict[str, bool])
async def verify_mfa(payload: MFARequest, service: AuthService = Depends(get_service)) -> dict[str, bool]:
    """Valida códigos TOTP enviados por el usuario."""

    return {"valid": service.verify_mfa(payload.email, payload.code)}


@router.get("/me", response_model=UserRead)
async def me(service: AuthService = Depends(get_service)) -> UserRead:
    """Retorna información del usuario autenticado."""

    user = service.bootstrap_admin(None)
    return UserRead.from_orm(user)
