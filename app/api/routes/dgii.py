"""DGII document submission endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.domain.models.acecf import ACECF
from app.domain.models.arecf import ARECF
from app.domain.models.ecf import ECF
from app.domain.models.rfce import RFCE
from app.security.xml import validate_with_xsd
from app.services.dgii_client import DGIIClient, get_dgii_client

router = APIRouter()


@router.post("/ecf/send")
async def send_ecf(payload: ECF, client: DGIIClient = Depends(get_dgii_client)) -> dict[str, str]:
    xml_bytes = payload.to_xml()
    validate_with_xsd(xml_bytes, "xsd/ecf.xsd")
    return await client.send_document(xml_bytes, document_type="ecf")


@router.post("/rfce/send")
async def send_rfce(payload: RFCE, client: DGIIClient = Depends(get_dgii_client)) -> dict[str, str]:
    xml_bytes = payload.to_xml()
    validate_with_xsd(xml_bytes, "xsd/rfce.xsd")
    return await client.send_document(xml_bytes, document_type="rfce")


@router.post("/acecf/send")
async def send_acecf(payload: ACECF, client: DGIIClient = Depends(get_dgii_client)) -> dict[str, str]:
    xml_bytes = payload.to_xml()
    validate_with_xsd(xml_bytes, "xsd/acecf.xsd")
    return await client.send_document(xml_bytes, document_type="acecf")


@router.post("/arecf/send")
async def send_arecf(payload: ARECF, client: DGIIClient = Depends(get_dgii_client)) -> dict[str, str]:
    xml_bytes = payload.to_xml()
    validate_with_xsd(xml_bytes, "xsd/arecf.xsd")
    return await client.send_document(xml_bytes, document_type="arecf")


@router.get("/status/{track_id}")
async def get_status(track_id: str, client: DGIIClient = Depends(get_dgii_client)) -> dict[str, str]:
    response = await client.get_status(track_id)
    if not response:
        raise HTTPException(status_code=404, detail="Track ID not found")
    return response
