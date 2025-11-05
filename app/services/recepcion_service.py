import base64
import asyncio
from typing import Union, Dict, Any, Optional
from datetime import datetime, timezone

from app.security.xml import validate_with_xsd
from app.security.xml_verify import verify_xml_signature

# Simple in-memory idempotency store for demo purposes
_IDEMPOTENCY_STORE: Dict[str, Dict[str, Any]] = {}

# XSD path stub
E_CF_XSD = "xsd/e_cf_v1_0.xsd"

async def _persist_ecf(xml_bytes: bytes, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    # Placeholder persistence: simulate async IO
    await asyncio.sleep(0.01)
    acuse = f"ARC-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}"
    return {"acuseId": acuse, "estado": "RECIBIDO", "detalle": "OK", "timestamp": datetime.now(timezone.utc).isoformat()}

async def procesar_ecf(payload: Union[str, bytes, dict], idempotency_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Procesa un e-CF. payload puede ser dict con 'ecf_xml_b64' o raw bytes/string.
    Se espera idempotency_key para garantizar idempotencia.
    """
    # Idempotency handling
    if idempotency_key:
        cached = _IDEMPOTENCY_STORE.get(idempotency_key)
        if cached:
            return cached

    # obtain xml bytes
    xml_bytes: Optional[bytes] = None
    if isinstance(payload, dict):
        if payload.get("ecf_xml_b64"):
            try:
                xml_bytes = base64.b64decode(payload["ecf_xml_b64"])
            except Exception as e:
                return {"error": f"ecf_xml_b64 decode error: {e}"}
        elif payload.get("ecf_json"):
            # naive conversion JSON -> XML for validation: here we wrap JSON as text inside XML root for demo
            import json as _json
            content = _json.dumps(payload["ecf_json"])
            xml_bytes = f"<ECF_JSON>{{content}}</ECF_JSON>".encode()
        else:
            return {"error": "Payload inválido: se requiere ecf_xml_b64 o ecf_json"}
    elif isinstance(payload, (bytes, bytearray)):
        xml_bytes = bytes(payload)
    elif isinstance(payload, str):
        xml_bytes = payload.encode()
    else:
        return {"error": "Tipo de payload no soportado"}

    # Validate with XSD
    try:
        validate_with_xsd(xml_bytes, E_CF_XSD)
    except Exception as e:
        return {"error": f"XSD validation failed: {e}"}

    # Verify signature
    try:
        if not verify_xml_signature(xml_bytes):
            return {"error": "Firma inválida"}
    except Exception as e:
        return {"error": f"Signature verification error: {e}"}

    # Persist and return acuse
    acuse = await _persist_ecf(xml_bytes, metadata=payload.get("metadata") if isinstance(payload, dict) else None)

    if idempotency_key:
        _IDEMPOTENCY_STORE[idempotency_key] = acuse

    return acuse
