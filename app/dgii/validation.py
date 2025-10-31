"""XML validation helpers using DGII XSD schemas."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, List

from lxml import etree

from app.dgii.exceptions import DGIIReceiptError

SCHEMAS_DIR = Path(__file__).resolve().parents[2] / "schemas"


def validate_xml(xml_bytes: bytes, xsd_name: str) -> None:
    """Validate XML against one of the DGII schemas.

    Raises:
        ValueError: when the XML does not comply with the schema.
        DGIIReceiptError: when the schema file is missing/unreadable.
    """

    xml_doc = etree.fromstring(xml_bytes)
    schema = _load_schema(xsd_name)

    if not schema.validate(xml_doc):
        errors = _collect_errors(schema.error_log)
        raise ValueError(f"XML inválido contra esquema {xsd_name}: {'; '.join(errors)}")


def _load_schema(xsd_name: str) -> etree.XMLSchema:
    path = SCHEMAS_DIR / xsd_name
    if not path.exists():
        raise DGIIReceiptError(f"No se encontró el esquema XSD requerido: {xsd_name}")

    try:
        schema_doc = etree.parse(str(path))
    except OSError as exc:
        raise DGIIReceiptError(f"No se pudo leer el esquema {xsd_name}") from exc
    return etree.XMLSchema(schema_doc)


def _collect_errors(errors: Iterable[etree._LogEntry]) -> List[str]:
    return [f"Linea {err.line}: {err.message}" for err in errors]
