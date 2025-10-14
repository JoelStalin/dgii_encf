"""Utilidades transversales."""
from __future__ import annotations

import base64
import hashlib
from typing import Iterable


def ensure_utf8(data: bytes) -> bytes:
    """Normaliza el contenido a UTF-8."""

    try:
        return data.decode("utf-8").encode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("El contenido debe estar codificado en UTF-8") from exc


def security_code_from_hash(signature_value: str) -> str:
    """Obtiene los primeros 6 caracteres del hash de firma."""

    digest = hashlib.sha256(signature_value.encode("utf-8")).hexdigest()
    return digest[:6].upper()


def chunked(iterable: Iterable, size: int):
    """Agrupa elementos de un iterable."""

    chunk = []
    for element in iterable:
        chunk.append(element)
        if len(chunk) == size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


def b64encode(data: bytes) -> str:
    """Codifica bytes a base64 sin saltos de línea."""

    return base64.b64encode(data).decode("ascii")
