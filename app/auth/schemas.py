"""Esquemas Pydantic para autenticación."""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class LoginRequest(BaseModel):
    """Solicitud de autenticación inicial."""

    email: EmailStr
    password: str = Field(min_length=8)


class LoginResponse(BaseModel):
    """Respuesta con tokens JWT."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class MFARequest(BaseModel):
    """Modelo para validar códigos MFA TOTP."""

    email: EmailStr
    code: str = Field(min_length=6, max_length=6)


class UserRead(BaseModel):
    """Información pública del usuario autenticado."""

    id: int
    email: EmailStr
    role: str

    model_config = ConfigDict(from_attributes=True)
