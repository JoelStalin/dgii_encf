"""Esquemas para servicios de firmado."""
from __future__ import annotations

from pydantic import BaseModel, Field


class SignXMLRequest(BaseModel):
    """Payload requerido para firmar un XML."""

    xml: str = Field(..., description="Documento XML sin firmar en base64")
    certificate_subject: str = Field(..., description="Nombre del sujeto del certificado")


class SignXMLResponse(BaseModel):
    """Respuesta con XML firmado."""

    xml_signed: str
    signature_value: str
    codigo_seguridad: str
