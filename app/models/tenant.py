"""Modelos relacionados con tenants."""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Tenant(Base):
    """Representa una empresa dentro del modelo multi-tenant."""

    __tablename__ = "tenants"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    rnc: Mapped[str] = mapped_column(String(11), nullable=False, unique=True)
    env: Mapped[str] = mapped_column(String(20), default="testecf")
    dgii_base_ecf: Mapped[str] = mapped_column(String(255))
    dgii_base_fc: Mapped[str] = mapped_column(String(255))
    cert_ref: Mapped[Optional[str]] = mapped_column(String(255))
    p12_kms_key: Mapped[Optional[str]] = mapped_column(String(255))

    certificates: Mapped[List["Certificate"]] = relationship(back_populates="tenant")
    users: Mapped[List["User"]] = relationship(back_populates="tenant")


class Delegation(Base):
    """Registra las delegaciones autorizadas ante la DGII."""

    __tablename__ = "delegations"

    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"))
    role: Mapped[str] = mapped_column(String(50))
    subject_rnc: Mapped[str] = mapped_column(String(11))
    xml_signed: Mapped[str] = mapped_column(String(512))
    status: Mapped[str] = mapped_column(String(20), default="pendiente")

    tenant: Mapped[Tenant] = relationship(backref="delegations")


class Certificate(Base):
    """Información de certificados digitales."""

    __tablename__ = "certificates"

    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"))
    alias: Mapped[str] = mapped_column(String(100), nullable=False)
    p12_path: Mapped[str] = mapped_column(String(255))
    not_before: Mapped[datetime]
    not_after: Mapped[datetime]
    issuer: Mapped[str] = mapped_column(String(255))
    subject: Mapped[str] = mapped_column(String(255))

    tenant: Mapped[Tenant] = relationship(back_populates="certificates")
