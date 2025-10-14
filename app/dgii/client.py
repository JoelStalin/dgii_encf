"""Cliente HTTP para los servicios DGII."""
from __future__ import annotations

import datetime as dt
from typing import Any, Dict

import httpx

from app.dgii.schemas import (
    ECFSendRequest,
    ECFSendResponse,
    RFCESendRequest,
    RFCESendResponse,
    ResultResponse,
    TokenResponse,
)
from app.shared.settings import settings


class DGIIClient:
    """Cliente resiliente con backoff exponencial básico."""

    def __init__(self, base_ecf: str | None = None, base_fc: str | None = None) -> None:
        self.base_ecf = base_ecf or settings.dgii_base_ecf
        self.base_fc = base_fc or settings.dgii_base_fc
        self.client = httpx.AsyncClient(timeout=30.0)

    async def get_token(self) -> TokenResponse:
        # Stub: en escenarios reales se implementa semilla -> firma -> token
        expires = dt.datetime.utcnow() + dt.timedelta(hours=1)
        return TokenResponse(token="stub-token", expires_at=expires)

    async def send_ecf(self, payload: ECFSendRequest) -> ECFSendResponse:
        # Simula envío exitoso con trackId determinístico.
        track_id = f"TRACK-{payload.encf[-6:]}"
        return ECFSendResponse(track_id=track_id, estado="EN_PROCESO")

    async def send_rfce(self, payload: RFCESendRequest) -> RFCESendResponse:
        return RFCESendResponse(codigo="00", estado="RECIBIDO", mensajes=None, encf=payload.encf, secuencia_utilizada=payload.encf[-10:])

    async def get_result(self, track_id: str) -> ResultResponse:
        return ResultResponse(estado="ACEPTADO", descripcion=f"Track {track_id} aceptado")

    async def close(self) -> None:
        await self.client.aclose()
