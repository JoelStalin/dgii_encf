"""Modelo de auditoría con hash encadenado."""
from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class AuditLog(Base):
    """Registra eventos auditables encadenados criptográficamente."""

    __tablename__ = "audit_logs"

    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"))
    actor: Mapped[str] = mapped_column(String(255))
    action: Mapped[str] = mapped_column(String(100))
    resource: Mapped[str] = mapped_column(String(255))
    hash_prev: Mapped[str] = mapped_column(String(128))
    hash_curr: Mapped[str] = mapped_column(String(128))
