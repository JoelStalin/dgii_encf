"""Modelos para almacenamiento de XML y representaciones impresas."""
from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class XMLStore(Base):
    """Repositorio de XML asociados a los comprobantes."""

    __tablename__ = "xml_store"

    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"))
    encf: Mapped[str] = mapped_column(String(20), index=True)
    kind: Mapped[str] = mapped_column(String(20))
    path: Mapped[str] = mapped_column(String(255))
    sha256: Mapped[str] = mapped_column(String(64))


class RIStore(Base):
    """Registra PDF de representación impresa."""

    __tablename__ = "ri_store"

    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"))
    encf: Mapped[str] = mapped_column(String(20), index=True)
    pdf_path: Mapped[str] = mapped_column(String(255))
    mode: Mapped[str] = mapped_column(String(20))
    hash: Mapped[str] = mapped_column(String(128))
