"""Rutas de integración DGII."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dgii.adapters import persist_ecf, persist_rfce
from app.dgii.client import DGIIClient
from app.dgii.schemas import (
    ECFSendRequest,
    ECFSendResponse,
    RFCESendRequest,
    RFCESendResponse,
    ResultResponse,
    TokenResponse,
)
from app.shared.database import get_db

router = APIRouter()


@router.get("/{tenant}/dgii/token", response_model=TokenResponse)
async def token(tenant: str) -> TokenResponse:
    client = DGIIClient()
    return await client.get_token()


@router.post("/{tenant}/dgii/ecf/send", response_model=ECFSendResponse)
async def send_ecf(tenant: int, payload: ECFSendRequest, db: Session = Depends(get_db)) -> ECFSendResponse:
    client = DGIIClient()
    response = await client.send_ecf(payload)
    persist_ecf(db, tenant, payload, response)
    return response


@router.post("/{tenant}/dgii/rfce/send", response_model=RFCESendResponse)
async def send_rfce(tenant: int, payload: RFCESendRequest, db: Session = Depends(get_db)) -> RFCESendResponse:
    client = DGIIClient()
    response = await client.send_rfce(payload)
    persist_rfce(db, tenant, payload, response)
    return response


@router.get("/{tenant}/dgii/ecf/result/{track_id}", response_model=ResultResponse)
async def result(tenant: int, track_id: str) -> ResultResponse:
    client = DGIIClient()
    return await client.get_result(track_id)
