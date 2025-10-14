"""Servicios de autenticación y emisión de tokens."""
from __future__ import annotations

import datetime as dt
import secrets

import pyotp
from fastapi import HTTPException, status

from app.auth.repository import AuthRepository
from app.auth.schemas import LoginResponse
from app.models.user import User
from app.shared.security import create_jwt, hash_password, verify_password
from app.shared.settings import settings


class AuthService:
    """Implementa reglas de negocio para autenticación."""

    def __init__(self, repository: AuthRepository) -> None:
        self.repository = repository

    def authenticate(self, email: str, password: str) -> tuple[User, LoginResponse]:
        user = self.repository.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

        access_payload = {"sub": str(user.id), "tenant_id": user.tenant_id, "role": user.role}
        refresh_payload = {"sub": str(user.id), "tenant_id": user.tenant_id, "scope": "refresh"}
        refresh_exp = dt.timedelta(minutes=settings.refresh_token_exp_minutes)
        return user, LoginResponse(access_token=create_jwt(access_payload), refresh_token=create_jwt(refresh_payload, refresh_exp))

    def verify_mfa(self, email: str, code: str) -> bool:
        user = self.repository.get_by_email(email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        totp = pyotp.TOTP(user.mfa_secret)
        return totp.verify(code, valid_window=1)

    def bootstrap_admin(self, db) -> User:
        """Crea un usuario administrador si no existen usuarios."""

        existing = self.repository.get_by_email("admin@getupnet.local")
        if existing:
            return existing
        admin = User(
            tenant_id=1,
            email="admin@getupnet.local",
            phone="0000000000",
            password_hash=hash_password("ChangeMe123!"),
            mfa_secret=pyotp.random_base32(),
            role="tenant_admin",
            status="activo",
        )
        return self.repository.create_user(admin)
