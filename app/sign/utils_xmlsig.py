"""Utilidades para firmado XMLDSig (representación conceptual)."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from lxml import etree


@dataclass
class SignatureResult:
    """Resultado del proceso de firma."""

    xml_signed: str
    certificate_subject: str
    signature_value: str


def load_xml(xml_content: bytes) -> etree._ElementTree:
    """Carga y valida que el XML tenga codificación UTF-8."""

    parser = etree.XMLParser(remove_blank_text=True, encoding="utf-8")
    return etree.fromstring(xml_content, parser=parser)


def sign_document(xml_content: bytes, certificate_subject: str) -> SignatureResult:
    """Simula el proceso de firmado XMLDSig.

    Este stub permite avanzar con las pruebas unitarias hasta integrar xmlsec.
    """

    root = load_xml(xml_content)
    signature_value = etree.tostring(root, encoding="utf-8").hex()[:64]
    signed_xml = etree.tostring(root, encoding="utf-8").decode("utf-8")
    return SignatureResult(xml_signed=signed_xml, certificate_subject=certificate_subject, signature_value=signature_value)
