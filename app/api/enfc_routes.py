# FILE: app/api/enfc_routes.py
"""FastAPI router exposing DGII ENFC validation endpoints."""
from __future__ import annotations

import json
import hashlib
from typing import Any, Dict, Tuple

from fastapi import APIRouter, Header, HTTPException, Request, Response, status
import structlog
from pydantic import ValidationError

from app.api.schemas.enfc_schemas import AprobacionReq, CertReq, RecepcionReq
from app.services.aprobacion_service import procesar_aprobacion
from app.services.auth_service import emitir_semilla, validar_certificado
from app.services.idempotency import idempotency_store
from app.services.recepcion_service import procesar_ecf

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/fe", tags=["ENFC"])

_ALLOWED_CONTENT_TYPES = {"application/json", "application/xml", "text/xml"}


def _normalize_content_type(raw: str | None) -> str:
    if not raw:
        return ""
    return raw.split(";", 1)[0].strip().lower()


def _hash_payload(content_type: str, body: bytes) -> str:
    if content_type == "application/json":
        try:
            parsed = json.loads(body.decode()) if body else {}
        except json.JSONDecodeError as exc:  # noqa: PERF203
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="JSON inválido") from exc
        canonical = json.dumps(parsed, sort_keys=True, separators=(",", ":")).encode()
        return hashlib.sha256(canonical).hexdigest()
    return hashlib.sha256(body).hexdigest()


async def _read_request(request: Request) -> Tuple[str, bytes]:
    content_type = _normalize_content_type(request.headers.get("content-type"))
    if content_type not in _ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Content-Type no soportado")
    body = await request.body()
    if not body:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cuerpo requerido")
    return content_type, body


async def _handle_idempotency(key: str, payload_hash: str, response: Response):
    try:
        cached = await idempotency_store.get(key, payload_hash)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    if cached:
        response.status_code = cached.status_code
        response.headers.update(cached.headers)
        response.headers["Idempotent-Replay"] = "true"
        return cached.body
    return None


async def _store_idempotent_response(
    key: str,
    payload_hash: str,
    status_code: int,
    body: Dict[str, Any],
    *,
    headers: Dict[str, str] | None = None,
) -> None:
    await idempotency_store.set(key, payload_hash, status_code, body, headers=headers)


@router.post("/recepcion/api/ecf")
async def recepcion_ecf(
    request: Request,
    response: Response,
    idempotency_key: str = Header(alias="Idempotency-Key"),
) -> Dict[str, Any]:
    if not idempotency_key:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Falta Idempotency-Key")

    content_type, body = await _read_request(request)
    payload_hash = _hash_payload(content_type, body)

    cached_body = await _handle_idempotency(idempotency_key, payload_hash, response)
    if cached_body is not None:
        return cached_body

    try:
        if content_type == "application/json":
            try:
                payload_dict = json.loads(body.decode())
                payload = RecepcionReq(**payload_dict).model_dump()
            except (json.JSONDecodeError, ValidationError) as exc:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"JSON inválido: {exc}") from exc
        else:
            payload = body
        result = await procesar_ecf(payload)
    except ValueError as exc:
        logger.warning("recepcion.ecf.error", error=str(exc))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    response.headers["Idempotent-Replay"] = "false"
    await _store_idempotent_response(
        idempotency_key,
        payload_hash,
        status.HTTP_200_OK,
        result,
        headers={"Content-Type": "application/json"},
    )
    return result


@router.post("/aprobacioncomercial/api/ecf")
async def aprobacion_ecf(
    request: Request,
    response: Response,
    idempotency_key: str = Header(alias="Idempotency-Key"),
) -> Dict[str, Any]:
    if not idempotency_key:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Falta Idempotency-Key")

    content_type, body = await _read_request(request)
    payload_hash = _hash_payload(content_type, body)

    cached_body = await _handle_idempotency(idempotency_key, payload_hash, response)
    if cached_body is not None:
        return cached_body

    try:
        if content_type == "application/json":
            try:
                payload_dict = json.loads(body.decode())
                payload = AprobacionReq(**payload_dict).model_dump()
            except (json.JSONDecodeError, ValidationError) as exc:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"JSON inválido: {exc}") from exc
        else:
            payload = body
        result = await procesar_aprobacion(payload)
    except ValueError as exc:
        logger.warning("aprobacion.ecf.error", error=str(exc))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    response.headers["Idempotent-Replay"] = "false"
    await _store_idempotent_response(
        idempotency_key,
        payload_hash,
        status.HTTP_200_OK,
        result,
        headers={"Content-Type": "application/json"},
    )
    return result


@router.get("/autenticacion/api/semilla")
async def obtener_semilla() -> Dict[str, Any]:
    return emitir_semilla()


@router.post("/autenticacion/api/validacioncertificado")
async def validacion_certificado(req: CertReq) -> Dict[str, Any]:
    return validar_certificado(req.model_dump())
