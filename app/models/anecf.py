"""Modelo para anulación de rangos."""
from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class ANECF(Base):
    """Registro de solicitudes de anulación."""

    __tablename__ = "anecf"

    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"))
    tipo_ecf: Mapped[str] = mapped_column(String(3))
    desde: Mapped[int] = mapped_column(Integer)
    hasta: Mapped[int] = mapped_column(Integer)
    cantidad: Mapped[int] = mapped_column(Integer)
    xml_path: Mapped[str] = mapped_column(String(255))
    estado_envio: Mapped[str] = mapped_column(String(20), default="pendiente")
