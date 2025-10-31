"""Pydantic model for RFCE."""
from __future__ import annotations

from datetime import date
from decimal import Decimal

from lxml import etree
from lxml.builder import E
from pydantic import BaseModel, Field


class RFCE(BaseModel):
    ENCF: str = Field(..., max_length=13)
    RNCEmisor: str = Field(..., max_length=11)
    Periodo: date
    MontoTotal: Decimal = Field(..., ge=0)

    def to_xml(self) -> bytes:
        doc = E.RFCE(
            E.ENCF(self.ENCF),
            E.RNCEmisor(self.RNCEmisor),
            E.Periodo(self.Periodo.isoformat()),
            E.MontoTotal(f"{self.MontoTotal:.2f}"),
        )
        return etree.tostring(doc, encoding="UTF-8", xml_declaration=True)
