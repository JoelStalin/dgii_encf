"""Dependencias de FastAPI para autenticación."""
from __future__ import annotations

from fastapi import Depends
from sqlalchemy.orm import Session

from app.auth.repository import AuthRepository
from app.auth.service import AuthService
from app.shared.database import get_db


def get_repository(db: Session = Depends(get_db)) -> AuthRepository:
    return AuthRepository(db)


def get_service(repository: AuthRepository = Depends(get_repository)) -> AuthService:
    return AuthService(repository)
