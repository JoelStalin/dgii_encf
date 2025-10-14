"""Modelo de resumen RFCE."""
from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class RFCESubmission(Base):
    """Registra los envíos RFCE a DGII."""

    __tablename__ = "rfce_submissions"

    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"))
    encf: Mapped[str] = mapped_column(String(20), index=True)
    resumen_xml_path: Mapped[str] = mapped_column(String(255))
    estado: Mapped[str] = mapped_column(String(30))
    mensajes: Mapped[str | None] = mapped_column(String(512))
    secuencia_utilizada: Mapped[str | None] = mapped_column(String(20))
