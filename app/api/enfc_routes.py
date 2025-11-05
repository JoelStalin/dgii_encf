from typing import Optional, Dict, Any
import base64
import json

from fastapi import APIRouter, Header, Request, HTTPException, Response, status
from pydantic import BaseModel

from app.services.recepcion_service import procesar_ecf
from app.services.aprobacion_service import procesar_aprobacion
from app.services.auth_service import emitir_semilla, validar_certificado

# Optional rate limit integration (slowapi). If not installed, no-op decorator.
try:
    from slowapi import Limiter
    from slowapi.util import get_remote_address
    limiter = Limiter(key_func=get_remote_address)
    rate_limit = limiter.limit("10/minute")
except Exception:
    def rate_limit(func):
        return func

# Structured logging
try:
    import structlog
    logger = structlog.get_logger("enfc_routes")
except Exception:
    import logging
    logger = logging.getLogger("enfc_routes")

router = APIRouter(prefix="/fe", tags=["ENFC"])

class RecepcionReq(BaseModel):
    formato: Optional[str] = None
    ecf_xml_b64: Optional[str] = None
    ecf_json: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

class AprobacionReq(BaseModel):
    aprobacion_xml_b64: Optional[str] = None
    aprobacion_json: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

class CertReq(BaseModel):
    cert_b64: Optional[str] = None
    p12_b64: Optional[str] = None
    password: Optional[str] = None

@router.post("/recepcion/api/ecf")
@rate_limit
async def recepcion_ecf(
    request: Request,
    Idempotency_Key: Optional[str] = Header(default=None, alias="Idempotency-Key"),
):
    if not Idempotency_Key:
        logger.warning("missing_idempotency", path="/recepcion/api/ecf")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Falta Idempotency-Key")

    content_type = (request.headers.get("content-type") or "").split(";")[0].strip()
    logger.info("recepcion.request", content_type=content_type, idempotency=Idempotency_Key)
    if content_type == "application/xml":
        body = await request.body()
        # encode XML body as base64 for service expectation
        payload = {"formato": "XML", "ecf_xml_b64": base64.b64encode(body).decode(), "metadata": {}}  
    elif content_type == "application/json" or content_type == "application/vnd.api+json":
        payload = await request.json()
    else:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Unsupported Content-Type")

    result = await procesar_ecf(payload, idempotency_key=Idempotency_Key)
    return result

@router.post("/aprobacioncomercial/api/ecf")
@rate_limit
async def aprobacion_ecf(
    request: Request,
    Idempotency_Key: Optional[str] = Header(default=None, alias="Idempotency-Key"),
):
    if not Idempotency_Key:
        logger.warning("missing_idempotency", path="/aprobacioncomercial/api/ecf")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Falta Idempotency-Key")

    content_type = (request.headers.get("content-type") or "").split(";")[0].strip()
    logger.info("aprobacion.request", content_type=content_type, idempotency=Idempotency_Key)
    if content_type == "application/xml":
        body = await request.body()
        payload = {"aprobacion_xml_b64": base64.b64encode(body).decode(), "metadata": {}}
    elif content_type == "application/json" or content_type == "application/vnd.api+json":
        payload = await request.json()
    else:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Unsupported Content-Type")

    result = await procesar_aprobacion(payload, idempotency_key=Idempotency_Key)
    return result

@router.get("/autenticacion/api/semilla")
@rate_limit
async def semilla():
    logger.info("semilla.request")
    return emitir_semilla()

@router.post("/autenticacion/api/validacioncertificado")
@rate_limit
async def validacion_cert(req: CertReq):
    logger.info("validacioncertificado.request")
    result = validar_certificado(req.model_dump())
    return result
