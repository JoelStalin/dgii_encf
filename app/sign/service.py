"""Servicio de firmado XMLDSig."""
from __future__ import annotations

import base64

from app.shared.utils import security_code_from_hash
from app.sign.schemas import SignXMLRequest, SignXMLResponse
from app.sign.utils_xmlsig import sign_document


class SignService:
    """Encapsula la lógica de firmado."""

    def sign(self, payload: SignXMLRequest) -> SignXMLResponse:
        xml_bytes = base64.b64decode(payload.xml)
        result = sign_document(xml_bytes, payload.certificate_subject)
        codigo_seguridad = security_code_from_hash(result.signature_value)
        return SignXMLResponse(xml_signed=result.xml_signed, signature_value=result.signature_value, codigo_seguridad=codigo_seguridad)
