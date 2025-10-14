"""Herramientas de trazabilidad distribuida."""
from __future__ import annotations

import uuid
from typing import Optional

from fastapi import Request

from app.shared.settings import settings


def ensure_trace_id(request: Request) -> str:
    """Garantiza la presencia de un identificador de traza por solicitud."""

    header = settings.tracing_header
    trace_id = request.headers.get(header)
    if not trace_id:
        trace_id = uuid.uuid4().hex
        request.state.generated_trace_id = trace_id
    return trace_id


def get_request_id(request: Request) -> Optional[str]:
    """Obtiene el identificador de la solicitud si existe."""

    return request.headers.get(settings.request_id_header)
