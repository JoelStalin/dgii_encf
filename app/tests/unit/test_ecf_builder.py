"""Pruebas del generador de e-CF."""
from __future__ import annotations

from app.billing.ecf_builder import build_ecf


def test_build_ecf_generates_xml() -> None:
    xml = build_ecf(encf="E310000000001", rnc_emisor="132456789", rnc_comprador="132456789", total=100.25)
    assert "<ENCF>E310000000001</ENCF>" in xml
