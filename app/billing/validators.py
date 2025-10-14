"""Validaciones para emisión de comprobantes."""
from __future__ import annotations

import re

RNC_REGEX = re.compile(r"^\d{9,11}$")
ENCF_REGEX = re.compile(r"^[A-Z]{1}\d{12}$")


def validate_rnc(value: str) -> None:
    if not RNC_REGEX.match(value):
        raise ValueError("RNC inválido")


def validate_encf(value: str) -> None:
    if not ENCF_REGEX.match(value):
        raise ValueError("ENCF inválido")
