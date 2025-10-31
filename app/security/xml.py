"""Secure XML parsing and schema validation helpers."""
from __future__ import annotations

from typing import Iterable

from defusedxml.lxml import fromstring as secure_fromstring
from lxml import etree

MAX_XML_BYTES = 2_000_000  # 2 MB
MAX_XML_DEPTH = 64


class XMLSecurityError(ValueError):
    """Raised when XML violates security policies."""


def _depth(node: etree._Element, level: int = 0) -> int:
    return max([level] + [_depth(child, level + 1) for child in node])


def parse_secure(xml_bytes: bytes) -> etree._Element:
    """Parse XML bytes with XXE protections and depth/size limits."""

    if len(xml_bytes) > MAX_XML_BYTES:
        raise XMLSecurityError("XML too large")
    root = secure_fromstring(xml_bytes)
    if _depth(root) > MAX_XML_DEPTH:
        raise XMLSecurityError("XML too deep")
    return root


def validate_with_xsd(xml_bytes: bytes, xsd_path: str) -> None:
    """Validate XML bytes with the provided XSD file."""

    root = parse_secure(xml_bytes)
    parser = etree.XMLParser(load_dtd=False, resolve_entities=False, no_network=True)
    schema_doc = etree.parse(xsd_path, parser)
    schema = etree.XMLSchema(schema_doc)
    schema.assertValid(root)


def ensure_elements(elements: Iterable[str], root: etree._Element) -> None:
    """Ensure required elements exist in an XML tree."""

    for element in elements:
        if root.find(element) is None:
            raise XMLSecurityError(f"Missing required element: {element}")
