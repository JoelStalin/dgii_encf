"""Secure XML utilities with lightweight schema checks."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

from defusedxml.ElementTree import fromstring as secure_fromstring
from xml.etree import ElementTree as ET

MAX_XML_BYTES = 2_000_000  # 2 MB
MAX_XML_DEPTH = 64


class XMLSecurityError(ValueError):
    """Raised when XML violates security policies."""


def _depth(node: ET.Element, level: int = 0) -> int:
    children = list(node)
    if not children:
        return level
    return max(_depth(child, level + 1) for child in children)


def parse_secure(xml_bytes: bytes) -> ET.Element:
    """Parse XML bytes with XXE protections and depth/size limits."""

    if len(xml_bytes) > MAX_XML_BYTES:
        raise XMLSecurityError("XML demasiado grande")

    root = secure_fromstring(xml_bytes)
    if _depth(root) > MAX_XML_DEPTH:
        raise XMLSecurityError("XML demasiado profundo")
    return root


def _require_paths(root: ET.Element, paths: Iterable[str]) -> None:
    for path in paths:
        if root.find(path) is None:
            raise XMLSecurityError(f"XML sin elemento requerido: {path}")


def validate_with_xsd(xml_bytes: bytes, xsd_path: str) -> None:
    """Validate XML bytes using lightweight checks derived from the schema name."""

    root = parse_secure(xml_bytes)
    schema_name = Path(xsd_path).name.lower()

    if schema_name == "ecf.xsd":
        if root.tag != "eCF":
            raise XMLSecurityError("XML e-CF debe tener raíz eCF")
        _require_paths(
            root,
            [
                "Encabezado",
                "Encabezado/ENCF",
                "Encabezado/RNCEmisor",
                "Detalle",
            ],
        )
    elif schema_name == "acecf.xsd":
        if root.tag != "ACECF":
            raise XMLSecurityError("XML de aprobación debe tener raíz ACECF")
        _require_paths(
            root,
            [
                "ENCF",
                "RNCEmisor",
                "RNCComprador",
                "Estado",
            ],
        )
    else:
        # For unknown schemas simply ensure the path exists to detect misconfiguration.
        Path(xsd_path).resolve(strict=True)


def ensure_elements(elements: Iterable[str], root: ET.Element) -> None:
    """Ensure required elements exist in an XML tree."""

    _require_paths(root, elements)
