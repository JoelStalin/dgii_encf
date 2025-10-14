"""Esquemas para comunicación con DGII."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TokenResponse(BaseModel):
    token: str
    expires_at: datetime


class ECFSendRequest(BaseModel):
    encf: str
    xml_signed: str


class ECFSendResponse(BaseModel):
    track_id: str
    estado: str


class RFCESendRequest(BaseModel):
    encf: str
    resumen_xml: str


class RFCESendResponse(BaseModel):
    """Respuesta estandarizada de la DGII para envíos RFCE."""

    model_config = ConfigDict(populate_by_name=True)

    codigo: str
    estado: str
    mensajes: Optional[str]
    encf: str
    secuencia_utilizada: Optional[str] = Field(None, alias="secuenciaUtilizada")


class ResultResponse(BaseModel):
    estado: str
    descripcion: Optional[str]
