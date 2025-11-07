"""Helpers to build DGII-compliant XML filenames."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Final

DEFAULT_AMBIENTE: Final = "PRECERT"


def build_xml_filename(
    document_type: str,
    rnc_emisor: str,
    encf: str,
    *,
    issued_at: datetime | None = None,
    ambiente: str | None = None,
) -> str:
    """Return a deterministic filename ``{TIPO}_{ENV}_{RNC}_{ENCF}_{TS}.xml``."""

    doc_type = _sanitize(document_type or "ECF")
    ambiente_value = _sanitize(ambiente or DEFAULT_AMBIENTE)
    issued = (issued_at or datetime.now(timezone.utc)).astimezone(timezone.utc).replace(microsecond=0)
    timestamp = issued.strftime("%Y%m%dT%H%M%SZ")
    rnc = "".join(ch for ch in rnc_emisor if ch.isdigit())
    encf_norm = _sanitize(encf)
    return f"{doc_type}_{ambiente_value}_{rnc}_{encf_norm}_{timestamp}.xml"


def _sanitize(value: str) -> str:
    return "".join(ch for ch in value.upper() if ch.isalnum() or ch == "-")
