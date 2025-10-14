"""Renderizado de representación impresa."""
from __future__ import annotations

import base64
from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

TEMPLATE_DIR = Path(__file__).parent / "templates"
_env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)), autoescape=select_autoescape(enabled_extensions=("html",)))


def render_html(*, encf: str, rnc_emisor: str, rnc_comprador: str, total: float, mode: str) -> str:
    template = _env.get_template("base.html")
    return template.render(
        encf=encf,
        rnc_emisor=rnc_emisor,
        rnc_comprador=rnc_comprador,
        total=f"{total:.2f}",
        mode=mode,
        generado_en=datetime.utcnow().isoformat(),
    )


def render_pdf_placeholder(html: str) -> str:
    """Devuelve una cadena base64 representando el PDF.

    Se utiliza un marcador hasta integrar una librería PDF segura.
    """

    return base64.b64encode(html.encode("utf-8")).decode("ascii")
