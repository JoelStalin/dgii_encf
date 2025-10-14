"""Modelo de acuse de recibo."""
from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Receipt(Base):
    """Modelo para ARECF."""

    __tablename__ = "receipts"

    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"))
    encf: Mapped[str] = mapped_column(String(20), index=True)
    rnc_emisor: Mapped[str] = mapped_column(String(11))
    rnc_comprador: Mapped[str] = mapped_column(String(11))
    estado: Mapped[str] = mapped_column(String(1))
    motivo_codigo: Mapped[str | None] = mapped_column(String(2))
