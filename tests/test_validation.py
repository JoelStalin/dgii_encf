from __future__ import annotations

from pathlib import Path

import pytest

from app.dgii.validation import validate_xml


def test_validate_xml_success() -> None:
    xml_bytes = Path("samples/ecf_valid.xml").read_bytes()
    validate_xml(xml_bytes, "ECF.xsd")


def test_validate_xml_failure() -> None:
    invalid_xml = b"""<?xml version='1.0' encoding='UTF-8'?><eCF><Encabezado><TipoECF>E31</TipoECF></Encabezado></eCF>"""
    with pytest.raises(ValueError):
        validate_xml(invalid_xml, "ECF.xsd")
