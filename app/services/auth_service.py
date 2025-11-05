import os
import base64
from datetime import datetime, timezone
from typing import Dict, Any, Optional

# Cryptography imports
try:
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.serialization import pkcs12
    from cryptography.hazmat.backends import default_backend
except Exception:
    x509 = None
    hashes = None
    pkcs12 = None
    default_backend = None

TTL = 300  # seconds

def _now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def emitir_semilla() -> Dict[str, Any]:
    nonce = base64.urlsafe_b64encode(os.urandom(12)).decode().rstrip("=")
    payload = f"{_now_iso()}:{nonce}".encode()
    semilla = base64.urlsafe_b64encode(payload).decode().rstrip("=")
    return {"semilla": semilla, "expiraEn": TTL}

def _fingerprint_sha256(cert) -> str:
    try:
        fp = cert.fingerprint(hashes.SHA256())
        return fp.hex().upper()
    except Exception:
        return ""

def validar_certificado(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recibe { cert_b64 } o { p12_b64, password }.
    Devuelve huella, subject, issuer, notBefore/notAfter y valido boolean.
    """
    try:
        if not x509:
            return {"valido": False, "detalle": "cryptography no disponible en el entorno"}

        cert = None
        if data.get("cert_b64"):
            raw = base64.b64decode(data["cert_b64"])
            # try PEM then DER
            try:
                cert = x509.load_pem_x509_certificate(raw, default_backend())
            except Exception:
                cert = x509.load_der_x509_certificate(raw, default_backend())
        elif data.get("p12_b64"):
            raw = base64.b64decode(data["p12_b64"])
            pwd = data.get("password")
            if pwd is None:
                pwd_bytes = None
            else:
                pwd_bytes = pwd.encode()
            try:
                pkcs = pkcs12.load_key_and_certificates(raw, pwd_bytes)
            except Exception as e:
                return {"valido": False, "detalle": f"P12 parse error: {e}"}
            if pkcs is None or pkcs[1] is None:
                return {"valido": False, "detalle": "P12 sin certificado"}
            cert = pkcs[1]
        else:
            return {"valido": False, "detalle": "Entrada vacía"}

        not_before = cert.not_valid_before.replace(tzinfo=timezone.utc).isoformat()
        not_after = cert.not_valid_after.replace(tzinfo=timezone.utc).isoformat()
        valido = datetime.now(timezone.utc) < cert.not_valid_after

        return {
            "valido": bool(valido),
            "huellaSha256": _fingerprint_sha256(cert),
            "subject": cert.subject.rfc4514_string(),
            "issuer": cert.issuer.rfc4514_string(),
            "notBefore": not_before,
            "notAfter": not_after,
            "detalle": "OK" if valido else "Certificado vencido"
        }
    except Exception as e:
        return {"valido": False, "detalle": f"Error: {e}"}
