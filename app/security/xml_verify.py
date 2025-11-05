"""XML digital signature verification helpers."""
from __future__ import annotations

from signxml import XMLVerifier

from app.security.xml import parse_secure


def verify_xml_signature(xml_bytes: bytes, *, require_x509: bool = False) -> bool:
    """Validate the XML signature using SignXML.

    Args:
        xml_bytes: The XML payload that must contain a Signature element.
        require_x509: If ``True`` the signature must contain an X509 certificate.

    Returns:
        ``True`` when the signature is valid, otherwise ``False``.
    """

    parse_secure(xml_bytes)  # Ensure document passes security guards first.
    try:
        verified = XMLVerifier().verify(xml_bytes)
    except Exception:
        return False
    if require_x509 and not verified.signed_xml.find(".//{*}X509Certificate"):
        return False
    return True
