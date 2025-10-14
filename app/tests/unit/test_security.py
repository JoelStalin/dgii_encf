"""Pruebas unitarias de seguridad."""
from __future__ import annotations

from app.shared.security import hash_password, verify_password


def test_password_roundtrip() -> None:
    hashed = hash_password("SuperSegura123!")
    assert verify_password("SuperSegura123!", hashed)
    assert not verify_password("otra", hashed)
