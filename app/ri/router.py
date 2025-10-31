"""FastAPI router for RI rendering."""
from __future__ import annotations

import base64

from fastapi import APIRouter, Query, status

from app.core.logging import bind_request_context
from app.ri.render import build_context, render_html, render_pdf
from app.ri.schemas import RIRequest

router = APIRouter(tags=["RI"])


@router.post("/render", status_code=status.HTTP_200_OK)
async def render_ri(
    payload: RIRequest,
    formato: str = Query("both", enum=["html", "pdf", "both"]),
) -> dict[str, str]:
    context = build_context(payload)
    bind_request_context(encf=context.encf, rnc=context.rnc_emisor, tipo_ecf="RI")
    response: dict[str, str] = {}

    if formato in {"html", "both"}:
        response["html"] = render_html(context)

    if formato in {"pdf", "both"}:
        pdf_bytes = render_pdf(context)
        response["pdf_base64"] = base64.b64encode(pdf_bytes).decode("ascii")

    response["qr_base64"] = context.qr_base64
    response["qr_url"] = context.qr_url
    return response
