"""Esquemas para APIs de recepción."""
from __future__ import annotations

from pydantic import BaseModel, Field


class ECFInbound(BaseModel):
    encf: str
    xml: str = Field(..., description="Documento XML recibido")


class ARECFInbound(BaseModel):
    encf: str
    estado: int = Field(..., ge=0, le=1)
    codigoMotivo: str | None = Field(None, max_length=1)


class ACECFInbound(BaseModel):
    encf: str
    estado: int = Field(..., ge=1, le=2)
    detalleMotivo: str | None = Field(None, max_length=255)
