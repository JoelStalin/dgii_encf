"""Pruebas del servicio de firmado."""
from __future__ import annotations

import base64

from app.sign.schemas import SignXMLRequest
from app.sign.service import SignService


def test_sign_service_generates_security_code() -> None:
    service = SignService()
    xml = """<?xml version='1.0'?><Factura><Monto>1</Monto></Factura>"""
    payload = SignXMLRequest(xml=base64.b64encode(xml.encode()).decode(), certificate_subject="CN=Prueba")
    response = service.sign(payload)
    assert len(response.codigo_seguridad) == 6
    assert response.xml_signed.startswith("<Factura")
