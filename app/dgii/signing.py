"""XML Digital Signature helpers for DGII e-CF flows."""
from __future__ import annotations

from pathlib import Path
from typing import Union

from cryptography.hazmat.primitives.serialization import pkcs12
from lxml import etree
from signxml import XMLSigner, methods

from app.dgii.exceptions import DGIISignError

XmlBytes = Union[bytes, bytearray]


def sign_ecf(xml_bytes: XmlBytes, p12_path: str, p12_password: str) -> bytes:
    """Sign an XML document with XMLDSig using RSA-SHA256.

    The DGII requires enveloped signatures that cover the full document (URI="").
    """

    try:
        root = etree.fromstring(xml_bytes)
    except etree.XMLSyntaxError as exc:
        raise DGIISignError(f"XML inválido: {exc}") from exc

    private_key, certificate = _load_credentials(p12_path, p12_password)

    signer = XMLSigner(
        method=methods.enveloped,
        signature_algorithm="rsa-sha256",
        digest_algorithm="sha256",
        c14n_algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315",
    )

    try:
        signed_root = signer.sign(root, key=private_key, cert=certificate)
    except Exception as exc:  # pragma: no cover - signxml raises varied exceptions
        raise DGIISignError("Error firmando el documento e-CF") from exc

    return etree.tostring(signed_root, encoding="utf-8", xml_declaration=True)


def _load_credentials(p12_path: str, password: str):
    """Load key and certificate from PKCS#12 bundle."""

    try:
        raw = Path(p12_path).read_bytes()
    except OSError as exc:
        raise DGIISignError(f"No se pudo leer el certificado en {p12_path}") from exc

    try:
        private_key, certificate, _additional = pkcs12.load_key_and_certificates(
            raw, password.encode("utf-8") if password else None
        )
    except Exception as exc:  # pragma: no cover - cryptography raises varied exceptions
        raise DGIISignError("Certificado inválido o contraseña incorrecta") from exc

    if not private_key or not certificate:
        raise DGIISignError("El certificado no contiene clave privada o certificado")

    return private_key, certificate
