from __future__ import annotations

import pytest
from httpx import URL

from app.security.http_client import SSRFProtectionError, _ensure_allowed  # type: ignore[attr-defined]


def test_disallow_non_allow_list_host() -> None:
    with pytest.raises(SSRFProtectionError):
        _ensure_allowed(URL("https://evil.example.com"))
