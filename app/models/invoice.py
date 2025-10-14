"""Modelo de comprobantes electrónicos."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.tenant import Tenant


class Invoice(Base):
    """Representa un e-CF emitido por la plataforma."""

    __tablename__ = "invoices"

    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"))
    encf: Mapped[str] = mapped_column(String(20), index=True)
    tipo_ecf: Mapped[str] = mapped_column(String(3))
    xml_path: Mapped[str] = mapped_column(String(255))
    xml_hash: Mapped[str] = mapped_column(String(128))
    estado_dgii: Mapped[str] = mapped_column(String(30), default="pendiente")
    track_id: Mapped[str | None] = mapped_column(String(64))
    codigo_seguridad: Mapped[str | None] = mapped_column(String(6))
    total: Mapped[float] = mapped_column(Numeric(16, 2))
    fecha_emision: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    tenant: Mapped[Tenant] = relationship(backref="invoices")
