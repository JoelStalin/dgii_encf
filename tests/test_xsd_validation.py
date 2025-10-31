from __future__ import annotations

from pathlib import Path

import pytest

from app.security.xml import XMLSecurityError, validate_with_xsd


@pytest.mark.parametrize(
    ("xml_path", "xsd_path"),
    [
        ("tests/assets/sample_ecf_32.xml", "xsd/ecf.xsd"),
        ("tests/assets/sample_acecf.xml", "xsd/acecf.xsd"),
        ("tests/assets/sample_arecf.xml", "xsd/arecf.xsd"),
        ("tests/assets/sample_rfce.xml", "xsd/rfce.xsd"),
    ],
)
def test_xml_validates(xml_path: str, xsd_path: str) -> None:
    xml_bytes = Path(xml_path).read_bytes()
    validate_with_xsd(xml_bytes, xsd_path)


def test_xml_too_large_raises() -> None:
    huge_xml = b"<eCF>" + b"<a>" * 1_000_000 + b"</a>" * 1_000_000 + b"</eCF>"
    with pytest.raises(XMLSecurityError):
        validate_with_xsd(huge_xml, "xsd/ecf.xsd")
