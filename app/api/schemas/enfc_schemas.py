# FILE: app/api/schemas/enfc_schemas.py
from pydantic import BaseModel
from typing import Optional, Dict

class RecepcionReq(BaseModel):
    formato: str
    ecf_xml_b64: Optional[str] = None
    ecf_json: Optional[Dict] = None
    metadata: Optional[Dict] = None

class AprobacionReq(BaseModel):
    aprobacion_xml_b64: Optional[str] = None
    aprobacion_json: Optional[Dict] = None
    metadata: Optional[Dict] = None

class CertReq(BaseModel):
    cert_b64: Optional[str] = None
    p12_b64: Optional[str] = None
    password: Optional[str] = None
