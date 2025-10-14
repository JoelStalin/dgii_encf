"""Operaciones de base de datos para autenticación."""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.user import User


class AuthRepository:
    """Envuelve consultas relacionadas con usuarios."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).one_or_none()

    def create_user(self, user: User) -> User:
        self.db.add(user)
        self.db.flush()
        return user
