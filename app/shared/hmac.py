"""Utilidades HMAC para comunicación interna segura."""
from __future__ import annotations

import hashlib
import hmac
from typing import Mapping

from app.shared.settings import settings


def sign_headers(headers: Mapping[str, str], body: bytes = b"") -> str:
    """Genera una firma HMAC-SHA256 con el secreto compartido."""

    canonical = "\n".join(f"{key.lower()}:{value.strip()}" for key, value in sorted(headers.items()))
    digest = hmac.new(settings.hmac_service_secret.encode("utf-8"), canonical.encode("utf-8") + body, hashlib.sha256)
    return digest.hexdigest()


def verify_signature(signature: str, headers: Mapping[str, str], body: bytes = b"") -> bool:
    """Verifica una firma HMAC-SHA256."""

    expected = sign_headers(headers, body)
    return hmac.compare_digest(signature, expected)
