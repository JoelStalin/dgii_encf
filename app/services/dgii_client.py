"""DGII HTTP client with signing and validation."""
from __future__ import annotations

from typing import Any, Optional

from app.infra.settings import settings
from app.security.http_client import get_json, post_xml
from app.security.signing import sign_xml_enveloped


class DGIIClient:
    """Wrapper around DGII services with cached token."""

    def __init__(self, token: Optional[str] = None):
        self.token = token

    async def ensure_token(self) -> str:
        if self.token:
            return self.token
        if not settings.dgii_token_url:
            raise RuntimeError("DGII token URL not configured")
        response = await get_json(str(settings.dgii_token_url), headers={})
        data = response.json()
        token = data.get("access_token")
        if not token:
            raise RuntimeError("DGII token missing from response")
        self.token = token
        return token

    async def send_document(self, xml_bytes: bytes, document_type: str) -> dict[str, Any]:
        token = await self.ensure_token()
        signed = sign_xml_enveloped(xml_bytes, settings.dgii_p12_path, settings.dgii_p12_password)

        if not settings.dgii_submission_url:
            raise RuntimeError("DGII submission URL not configured")

        url = f"{settings.dgii_submission_url.rstrip('/')}/{document_type}"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/xml"}
        response = await post_xml(url, signed, headers=headers)
        return response.json()

    async def get_status(self, track_id: str) -> dict[str, Any]:
        token = await self.ensure_token()
        if not settings.dgii_status_url:
            raise RuntimeError("DGII status URL not configured")
        url = f"{settings.dgii_status_url.rstrip('/')}/{track_id}"
        headers = {"Authorization": f"Bearer {token}"}
        response = await get_json(url, headers=headers)
        return response.json()


async def get_dgii_client() -> DGIIClient:
    return DGIIClient()
