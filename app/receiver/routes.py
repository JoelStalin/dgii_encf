"""API que simula recepción DGII."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.receiver.schemas import ACECFInbound, ARECFInbound, ECFInbound
from app.receiver.validators import XMLValidationError, validate_xml

router = APIRouter()


@router.post("/{tenant}/recv/ecf")
async def recv_ecf(tenant: int, payload: ECFInbound) -> dict[str, str]:
    try:
        validate_xml(payload.xml)
    except XMLValidationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return {"encf": payload.encf, "status": "recibido"}


@router.post("/{tenant}/recv/ack")
async def recv_ack(tenant: int, payload: ARECFInbound) -> dict[str, str | int]:
    if payload.estado == 1 and not payload.codigoMotivo:
        raise HTTPException(status_code=400, detail="Debe indicar código de motivo cuando el estado es No Recibido")
    return {"encf": payload.encf, "estado": payload.estado}


@router.post("/{tenant}/recv/approval")
async def recv_approval(tenant: int, payload: ACECFInbound) -> dict[str, str | int]:
    if payload.estado == 2 and not payload.detalleMotivo:
        raise HTTPException(status_code=400, detail="Debe indicar detalle de motivo cuando se rechaza")
    return {"encf": payload.encf, "estado": payload.estado}
