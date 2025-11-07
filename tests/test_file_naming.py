from __future__ import annotations

from datetime import datetime, timezone

from app.dgii.file_naming import build_xml_filename


def test_build_xml_filename_normalizes_values() -> None:
    issued = datetime(2024, 5, 1, 12, 30, tzinfo=timezone.utc)
    name = build_xml_filename("ecf", "1-31-415161", "e310000000001", issued_at=issued, ambiente="precert")
    assert name == "ECF_PRECERT_131415161_E310000000001_20240501T123000Z.xml"
