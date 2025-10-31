"""Renderizado de representación impresa."""
from __future__ import annotations

import base64
from dataclasses import asdict, dataclass
from io import BytesIO
from pathlib import Path

import qrcode
from jinja2 import Environment, FileSystemLoader, select_autoescape
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from app.core.config import settings
from app.ri.schemas import RIRequest


TEMPLATE_DIR = Path(__file__).parent / "templates"
_env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)), autoescape=select_autoescape(enabled_extensions=("html",)))


@dataclass
class RIContext:
    encf: str
    rnc_emisor: str
    razon_social_emisor: str
    rnc_receptor: str
    razon_social_receptor: str
    monto_total: str
    fecha_emision: str
    items: list[dict[str, str]]
    qr_base64: str
    qr_url: str
    direccion_emisor: str | None = None
    direccion_receptor: str | None = None


def build_context(request: RIRequest) -> RIContext:
    qr_url = request.qr_url or f"{settings.ri_qr_base_url}?encf={request.encf}&rnc={request.rnc_emisor}"
    qr_base64 = _generate_qr_base64(qr_url)
    items = [
        {
            "descripcion": item.descripcion,
            "cantidad": f"{item.cantidad:.2f}",
            "precio_unitario": f"{item.precio_unitario:.2f}",
            "total": f"{item.total:.2f}",
        }
        for item in request.items
    ]

    return RIContext(
        encf=request.encf,
        rnc_emisor=request.rnc_emisor,
        razon_social_emisor=request.razon_social_emisor,
        rnc_receptor=request.rnc_receptor,
        razon_social_receptor=request.razon_social_receptor,
        monto_total=f"{request.monto_total:.2f}",
        fecha_emision=request.fecha_emision.isoformat(),
        items=items,
        qr_base64=qr_base64,
        qr_url=qr_url,
        direccion_emisor=request.direccion_emisor,
        direccion_receptor=request.direccion_receptor,
    )


def render_html(context: RIContext) -> str:
    template = _env.get_template("ri_default.html")
    return template.render(**asdict(context))


def render_pdf(context: RIContext) -> bytes:
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle(f"RI-{context.encf}")
    margin = 20 * mm
    width, height = letter
    y = height - margin

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(margin, y, "Representación Impresa e-CF")
    y -= 12
    pdf.setFont("Helvetica", 10)
    pdf.drawString(margin, y, f"ENCF: {context.encf}")
    y -= 12
    pdf.drawString(margin, y, f"Fecha emisión: {context.fecha_emision}")
    y -= 18

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(margin, y, "Emisor")
    y -= 12
    pdf.setFont("Helvetica", 10)
    pdf.drawString(margin, y, f"RNC: {context.rnc_emisor}")
    y -= 12
    pdf.drawString(margin, y, context.razon_social_emisor)
    if context.direccion_emisor:
        y -= 12
        pdf.drawString(margin, y, context.direccion_emisor)
    y -= 18

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(margin, y, "Receptor")
    y -= 12
    pdf.setFont("Helvetica", 10)
    pdf.drawString(margin, y, f"RNC: {context.rnc_receptor}")
    y -= 12
    pdf.drawString(margin, y, context.razon_social_receptor)
    if context.direccion_receptor:
        y -= 12
        pdf.drawString(margin, y, context.direccion_receptor)
    y -= 18

    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(margin, y, "Detalle")
    pdf.setFont("Helvetica", 9)
    y -= 12
    for item in context.items:
        pdf.drawString(margin, y, f"{item['descripcion']} x{item['cantidad']} @ {item['precio_unitario']} = {item['total']}")
        y -= 10
        if y < margin + 50:
            pdf.showPage()
            y = height - margin
            pdf.setFont("Helvetica", 9)

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(margin, y, f"Total: {context.monto_total} DOP")

    qr_image = ImageReader(BytesIO(base64.b64decode(context.qr_base64)))
    pdf.drawImage(qr_image, width - 50 * mm, margin, width=40 * mm, height=40 * mm)
    pdf.setFont("Helvetica", 8)
    pdf.drawString(width - 50 * mm, margin + 42 * mm, "Escanea para validar")

    pdf.showPage()
    pdf.save()
    return buffer.getvalue()


def _generate_qr_base64(data: str) -> str:
    qr = qrcode.QRCode(box_size=4, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("ascii")
