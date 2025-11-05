import base64
import asyncio
from typing import Union, Dict, Any, Optional

from app.security.xml import validate_with_xsd

# In-memory idempotency store for approvals
_APRO_SINGLETON: Dict[str, Dict[str, Any]] = {}

APROBACION_XSD = "xsd/aprobacion_v1_0.xsd"

async def _persist_aprobacion(xml_bytes: bytes, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    await asyncio.sleep(0.01)
    return {"acuseId": "AC-001", "estado": "ACEPTADO", "detalle": "OK"}

async def procesar_aprobacion(payload: Union[str, bytes, dict], idempotency_key: Optional[str] = None) -> Dict[str, Any]:
    if idempotency_key:
        cached = _APRO_SINGLETON.get(idempotency_key)
        if cached:
            return cached

    xml_bytes: Optional[bytes] = None
    if isinstance(payload, dict):
        if payload.get("aprobacion_xml_b64"):
            try:
                xml_bytes = base64.b64decode(payload["aprobacion_xml_b64"])
            except Exception as e:
                return {"error": f"aprobacion_xml_b64 decode error: {e}"}
        elif payload.get("aprobacion_json"):
            import json as _json
            content = _json.dumps(payload["aprobacion_json"])
            xml_bytes = f"<APROBACION_JSON>{{content}}</APROBACION_JSON>".encode()
        else:
            return {"error": "Payload inválido: se requiere aprobacion_xml_b64 o aprobacion_json"}
    elif isinstance(payload, (bytes, bytearray)):
        xml_bytes = bytes(payload)
    elif isinstance(payload, str):
        xml_bytes = payload.encode()
    else:
        return {"error": "Tipo de payload no soportado"}

    # Validate with XSD
    try:
        validate_with_xsd(xml_bytes, APROBACION_XSD)
    except Exception as e:
        return {"error": f"XSD validation failed: {e}"}

    result = await _persist_aprobacion(xml_bytes, metadata=payload.get("metadata") if isinstance(payload, dict) else None)
    if idempotency_key:
        _APRO_SINGLETON[idempotency_key] = result
    return result
