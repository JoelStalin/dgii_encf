"""DGII ENFC reception service handling validation and persistence stubs."""
from __future__ import annotations

import base64
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Union
from xml.etree.ElementTree import Element, SubElement, tostring

import structlog

from app.security.xml import validate_with_xsd
from app.security.xml_verify import verify_xml_signature

logger = structlog.get_logger(__name__)

_ECF_XSD_PATH = "xsd/ecf.xsd"


def _populate_node(node: Element, value: Any) -> None:
    if isinstance(value, dict):
        for child_key, child_value in value.items():
            if isinstance(child_value, list):
                for entry in child_value:
                    child = SubElement(node, child_key)
                    _populate_node(child, entry)
            else:
                child = SubElement(node, child_key)
                _populate_node(child, child_value)
    elif value is not None:
        node.text = str(value)


def _dict_to_xml(payload: Dict[str, Any], root_name: str = "eCF") -> bytes:
    root = Element(root_name)
    _populate_node(root, payload)
    return tostring(root, encoding="utf-8")


def _extract_xml_bytes(payload: Union[str, bytes, Dict[str, Any]]) -> bytes:
    if isinstance(payload, bytes):
        return payload
    if isinstance(payload, str):
        return payload.encode("utf-8")
    if isinstance(payload, dict):
        if xml_b64 := payload.get("ecf_xml_b64"):
            return base64.b64decode(xml_b64)
        if xml_dict := payload.get("ecf_json"):
            return _dict_to_xml(xml_dict)
    raise ValueError("Unsupported payload format for e-CF reception")


async def procesar_ecf(payload: Union[str, bytes, Dict[str, Any]]) -> Dict[str, Any]:
    """Validate and persist the incoming e-CF payload, returning an acknowledgement."""

    xml_bytes = _extract_xml_bytes(payload)
    logger.info("recepcion.ecf.decoded", size=len(xml_bytes))

    validate_with_xsd(xml_bytes, _ECF_XSD_PATH)
    if not verify_xml_signature(xml_bytes):
        logger.warning("recepcion.ecf.signature_invalid")
        raise ValueError("Firma inválida del documento e-CF")

    acuse_id = f"ARC-{uuid.uuid4().hex[:12].upper()}"
    timestamp = datetime.now(timezone.utc).isoformat()
    logger.info("recepcion.ecf.persisted", acuse_id=acuse_id)

    return {
        "acuseId": acuse_id,
        "estado": "RECIBIDO",
        "detalle": "OK",
        "timestamp": timestamp,
    }
