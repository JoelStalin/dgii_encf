"""DGII ENFC authentication helpers for semilla issuance and certificate checks."""
from __future__ import annotations

import base64
import secrets
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

import structlog
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import pkcs12

logger = structlog.get_logger(__name__)

_SEMILLA_TTL_SECONDS = 300
_semillas: Dict[str, datetime] = {}


def _now() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def emitir_semilla() -> Dict[str, object]:
    """Issue a short-lived DGII seed."""

    issued_at = _now()
    nonce = secrets.token_urlsafe(16)
    payload = f"{issued_at.isoformat()}:{nonce}".encode()
    semilla = base64.urlsafe_b64encode(payload).decode().rstrip("=")
    _semillas[semilla] = issued_at + timedelta(seconds=_SEMILLA_TTL_SECONDS)
    logger.info("auth.semilla.emitida", expira_en=_SEMILLA_TTL_SECONDS)
    return {"semilla": semilla, "expiraEn": _SEMILLA_TTL_SECONDS}


def _load_certificate(cert_bytes: bytes) -> x509.Certificate:
    try:
        return x509.load_pem_x509_certificate(cert_bytes, default_backend())
    except ValueError:
        return x509.load_der_x509_certificate(cert_bytes, default_backend())


def _load_from_pkcs12(p12_bytes: bytes, password: Optional[str]) -> x509.Certificate:
    _key, cert, _chain = pkcs12.load_key_and_certificates(
        p12_bytes,
        password.encode() if password else None,
        backend=default_backend(),
    )
    if not cert:
        raise ValueError("PKCS12 file does not contain a certificate")
    return cert


def _fingerprint_sha256(cert: x509.Certificate) -> str:
    return cert.fingerprint(hashes.SHA256()).hex().upper()


def validar_certificado(data: Dict[str, Optional[str]]) -> Dict[str, object]:
    """Validate a certificate or PKCS12 payload and return metadata."""

    try:
        cert: Optional[x509.Certificate] = None
        if data.get("cert_b64"):
            cert_bytes = base64.b64decode(data["cert_b64"])
            cert = _load_certificate(cert_bytes)
        elif data.get("p12_b64"):
            cert_bytes = base64.b64decode(data["p12_b64"])
            cert = _load_from_pkcs12(cert_bytes, data.get("password"))
        else:
            return {"valido": False, "detalle": "Entrada vacía"}

        now = _now()
        not_before = cert.not_valid_before.replace(tzinfo=timezone.utc)
        not_after = cert.not_valid_after.replace(tzinfo=timezone.utc)
        valido = not_before <= now <= not_after

        response = {
            "valido": bool(valido),
            "huellaSha256": _fingerprint_sha256(cert),
            "subject": cert.subject.rfc4514_string(),
            "issuer": cert.issuer.rfc4514_string(),
            "notBefore": not_before.isoformat(),
            "notAfter": not_after.isoformat(),
            "detalle": "OK" if valido else "Certificado vencido",
        }
        logger.info("auth.certificado.validado", valido=valido)
        return response
    except Exception as exc:  # noqa: BLE001
        logger.warning("auth.certificado.error", error=str(exc))
        return {"valido": False, "detalle": f"Error: {exc}"}
