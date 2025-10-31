"""Asynchronous HTTP client for DGII services."""
from __future__ import annotations

import asyncio
import uuid
from datetime import datetime
from typing import Any, Dict, Optional

import httpx
from httpx import AsyncClient, HTTPError, HTTPStatusError
from lxml import etree

from app.core.config import Settings, settings
from app.core.logging import bind_request_context
from app.dgii.exceptions import DGIIAuthError, DGIIReceiptError, DGIIRetryableError
from app.dgii.retry import async_retry


class DGIIClient:
    """High-level DGII client covering authentication and submissions."""

    def __init__(
        self,
        *,
        config: Settings | None = None,
        client: AsyncClient | None = None,
    ) -> None:
        self.config = config or settings
        self._client = client or AsyncClient(timeout=self.config.dgii_http_timeout_seconds)
        self._own_client = client is None
        self._auth_base = self.config.url_for("auth")
        self._recepcion_base = self.config.url_for("recepcion")
        self._recepcion_fc_base = self.config.url_for("recepcion_fc")

    async def __aenter__(self) -> "DGIIClient":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

    async def close(self) -> None:
        if self._own_client:
            await self._client.aclose()

    async def get_seed(self) -> bytes:
        """Fetch XML seed from DGII authentication service."""

        url = f"{self._auth_base}/semilla"
        response = await self._request("GET", url)
        return response.content

    def sign_seed(self, seed_xml: bytes) -> bytes:
        """Sign the seed XML using the configured certificate."""

        from app.dgii.signing import sign_ecf

        return sign_ecf(seed_xml, str(self.config.dgii_cert_p12_path), self.config.dgii_cert_p12_password)

    async def get_token(self, signed_seed_xml: bytes) -> Dict[str, Any]:
        """Exchange signed seed for a bearer token."""

        url = f"{self._auth_base}/token"
        response = await self._request(
            "POST",
            url,
            content=signed_seed_xml,
            headers={"Content-Type": "application/xml"},
        )

        try:
            payload = response.json()
        except ValueError as exc:
            raise DGIIAuthError("Respuesta inválida al obtener token") from exc

        token = payload.get("access_token") or payload.get("token")
        expires = payload.get("expires_at") or payload.get("expiration")
        if not token or not expires:
            raise DGIIAuthError("La respuesta de token no contiene campos requeridos")
        return {"access_token": token, "expires_at": expires}

    async def send_ecf(self, xml_bytes: bytes, token: str) -> Dict[str, Any]:
        url = f"{self._recepcion_base}/ecf"
        return await self._submit(url, xml_bytes, token)

    async def send_rfce(self, xml_bytes: bytes, token: str) -> Dict[str, Any]:
        url = f"{self._recepcion_fc_base}/rfce"
        return await self._submit(url, xml_bytes, token)

    async def send_anecf(self, xml_bytes: bytes, token: str) -> Dict[str, Any]:
        url = f"{self._recepcion_base}/anecf"
        return await self._submit(url, xml_bytes, token)

    async def send_acecf(self, xml_bytes: bytes, token: str) -> Dict[str, Any]:
        url = f"{self._recepcion_base}/acecf"
        return await self._submit(url, xml_bytes, token)

    async def send_arecf(self, xml_bytes: bytes, token: str) -> Dict[str, Any]:
        url = f"{self._recepcion_base}/arecef"
        return await self._submit(url, xml_bytes, token)

    async def get_status(self, track_id: str, token: str) -> Dict[str, Any]:
        url = f"{self._recepcion_base}/estatus/{track_id}"
        response = await self._request(
            "GET",
            url,
            headers=self._auth_headers(token),
        )
        return self._parse_payload(response)

    async def _submit(self, url: str, xml_bytes: bytes, token: str) -> Dict[str, Any]:
        headers = {"Content-Type": "application/xml", **self._auth_headers(token)}
        headers.update(self._idempotency_headers())
        response = await self._request("POST", url, content=xml_bytes, headers=headers)
        payload = self._parse_payload(response)
        return payload

    async def _request(
        self,
        method: str,
        url: str,
        *,
        headers: Optional[Dict[str, str]] = None,
        content: bytes | None = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> httpx.Response:
        """Perform an HTTP request with retries."""

        logger = bind_request_context(url=url, method=method)
        retries = self.config.dgii_http_retries
        async for attempt in async_retry(retries):
            with attempt:
                try:
                    response = await self._client.request(
                        method,
                        url,
                        headers=headers,
                        content=content,
                        params=params,
                    )
                    response.raise_for_status()
                    logger.info("DGII HTTP OK", status_code=response.status_code)
                    return response
                except HTTPStatusError as exc:
                    status_code = exc.response.status_code
                    body = exc.response.text
                    logger.warning("DGII HTTP error", status_code=status_code, body=body[:250])
                    if 400 <= status_code < 500:
                        raise DGIIReceiptError(f"DGII rechazó la solicitud ({status_code})") from exc
                    raise
                except HTTPError as exc:
                    logger.warning("DGII HTTP transitorio", error=str(exc))
                    raise DGIIRetryableError("Error de comunicación con DGII") from exc

        raise RuntimeError("Reintentos agotados para llamada DGII")  # pragma: no cover

    def _auth_headers(self, token: str) -> Dict[str, str]:
        return {"Authorization": f"Bearer {token}"}

    def _idempotency_headers(self) -> Dict[str, str]:
        return {"Idempotency-Key": str(uuid.uuid4())}

    def _parse_payload(self, response: httpx.Response) -> Dict[str, Any]:
        if response.headers.get("Content-Type", "").startswith("application/xml"):
            return self._parse_xml_payload(response.content)
        try:
            return response.json()
        except ValueError:
            return {"raw": response.text}

    def _parse_xml_payload(self, content: bytes) -> Dict[str, Any]:
        try:
            root = etree.fromstring(content)
        except etree.XMLSyntaxError:
            return {"raw": content.decode("utf-8", "ignore")}
        payload: Dict[str, Any] = {}
        for child in root.iterchildren():
            payload[child.tag.lower()] = child.text
        return payload
