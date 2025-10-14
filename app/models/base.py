"""Declaraciones base de SQLAlchemy 2."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base para todos los modelos con columnas comunes."""

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    @declared_attr.directive
    def __tablename__(cls) -> str:  # type: ignore[override]
        return cls.__name__.lower()
