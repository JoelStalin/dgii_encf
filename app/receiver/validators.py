"""Validaciones de negocio para recepción."""
from __future__ import annotations

from lxml import etree


class XMLValidationError(ValueError):
    pass


def validate_xml(xml: str) -> None:
    """Verifica que el XML sea bien formado y no contenga tags vacíos."""

    root = etree.fromstring(xml.encode("utf-8"))
    for element in root.iter():
        if element.text is not None and element.text.strip() == "" and not list(element):
            raise XMLValidationError("Los elementos vacíos no están permitidos")
