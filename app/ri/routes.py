"""Rutas para representación impresa."""
from __future__ import annotations

from fastapi import APIRouter

from app.ri.render import render_html, render_pdf_placeholder

router = APIRouter()


@router.post("/{tenant}/ri/render")
async def render_ri(tenant: int, payload: dict) -> dict:
    html = render_html(
        encf=payload["encf"],
        rnc_emisor=payload["rnc_emisor"],
        rnc_comprador=payload["rnc_comprador"],
        total=float(payload["total"]),
        mode=payload.get("mode", "diferido"),
    )
    pdf_b64 = render_pdf_placeholder(html)
    return {"html": html, "pdf_base64": pdf_b64}
