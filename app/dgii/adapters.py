"""Adaptadores para persistir resultados DGII."""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.dgii.schemas import ECFSendRequest, ECFSendResponse, RFCESendRequest, RFCESendResponse
from app.models.invoice import Invoice
from app.models.rfce import RFCESubmission


def persist_ecf(session: Session, tenant_id: int, request: ECFSendRequest, response: ECFSendResponse) -> Invoice:
    invoice = Invoice(
        tenant_id=tenant_id,
        encf=request.encf,
        tipo_ecf=request.encf[5:7],
        xml_path=f"xml/{request.encf}.xml",
        xml_hash="stub",
        estado_dgii=response.estado,
        track_id=response.track_id,
        codigo_seguridad="000000",
        total=0,
    )
    session.add(invoice)
    session.flush()
    return invoice


def persist_rfce(session: Session, tenant_id: int, request: RFCESendRequest, response: RFCESendResponse) -> RFCESubmission:
    rfce = RFCESubmission(
        tenant_id=tenant_id,
        encf=request.encf,
        resumen_xml_path=f"rfce/{request.encf}.xml",
        estado=response.estado,
        mensajes=response.mensajes,
        secuencia_utilizada=response.secuencia_utilizada,
    )
    session.add(rfce)
    session.flush()
    return rfce
