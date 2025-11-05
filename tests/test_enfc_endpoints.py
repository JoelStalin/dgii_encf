"""Integration tests for ENFC FastAPI endpoints."""
from __future__ import annotations

import asyncio
import base64
from pathlib import Path

import pytest
from httpx import AsyncClient

from app.main import app
from app.services.idempotency import idempotency_store

ECF_SAMPLE = Path("tests/assets/sample_ecf_32.xml").read_bytes()
APROBACION_SAMPLE_PATH = Path("tests/assets/sample_acecf.xml")
APROBACION_SAMPLE = (
    APROBACION_SAMPLE_PATH.read_bytes()
    if APROBACION_SAMPLE_PATH.exists()
    else b"<ACECF><ENCF>E310000000000</ENCF><RNCEmisor>101010101</RNCEmisor><RNCComprador>102030405</RNCComprador><Estado>ACEPTADO</Estado><Motivo>OK</Motivo><FechaAprobacion>2024-01-01T00:00:00Z</FechaAprobacion></ACECF>"
)


@pytest.fixture(autouse=True)
def _clear_idempotency():
    asyncio.run(idempotency_store.clear())
    yield
    asyncio.run(idempotency_store.clear())


def test_semilla_returns_seed():
    async def _run() -> None:
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/fe/autenticacion/api/semilla")
        data = response.json()
        assert response.status_code == 200
        assert "semilla" in data
        assert data["expiraEn"] == 300

    asyncio.run(_run())


def test_validacion_certificado_input_vacio():
    async def _run() -> None:
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/fe/autenticacion/api/validacioncertificado",
                json={},
            )
        assert response.status_code == 200
        assert response.json()["valido"] is False

    asyncio.run(_run())


def test_recepcion_ecf_requires_idempotency_header():
    async def _run() -> None:
        payload = {
            "formato": "XML",
            "ecf_xml_b64": base64.b64encode(ECF_SAMPLE).decode(),
        }
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post("/fe/recepcion/api/ecf", json=payload)
        assert response.status_code == 400
        assert response.json()["detail"] == "Falta Idempotency-Key"

    asyncio.run(_run())


def test_recepcion_ecf_success(monkeypatch):
    async def _run() -> None:
        monkeypatch.setattr("app.services.recepcion_service.verify_xml_signature", lambda _xml: True)
        payload = {
            "formato": "XML",
            "ecf_xml_b64": base64.b64encode(ECF_SAMPLE).decode(),
        }
        headers = {"Idempotency-Key": "abc123"}
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/fe/recepcion/api/ecf",
                json=payload,
                headers=headers,
            )
            replay = await client.post(
                "/fe/recepcion/api/ecf",
                json=payload,
                headers=headers,
            )
        assert response.status_code == 200
        data = response.json()
        assert data["estado"] == "RECIBIDO"
        assert replay.headers.get("Idempotent-Replay") == "true"
        assert replay.json() == data

    asyncio.run(_run())


def test_recepcion_ecf_invalid_signature(monkeypatch):
    async def _run() -> None:
        monkeypatch.setattr("app.services.recepcion_service.verify_xml_signature", lambda _xml: False)
        payload = {
            "formato": "XML",
            "ecf_xml_b64": base64.b64encode(ECF_SAMPLE).decode(),
        }
        headers = {"Idempotency-Key": "key-invalid"}
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/fe/recepcion/api/ecf",
                json=payload,
                headers=headers,
            )
        assert response.status_code == 400
        assert "Firma inválida" in response.json()["detail"]

    asyncio.run(_run())


def test_aprobacion_ecf_success(monkeypatch):
    async def _run() -> None:
        monkeypatch.setattr("app.security.xml.validate_with_xsd", lambda *_args, **_kwargs: None)
        payload = {
            "aprobacion_xml_b64": base64.b64encode(APROBACION_SAMPLE).decode(),
        }
        headers = {"Idempotency-Key": "approv-1"}
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/fe/aprobacioncomercial/api/ecf",
                json=payload,
                headers=headers,
            )
        assert response.status_code == 200
        assert response.json()["estado"] == "ACEPTADO"

    asyncio.run(_run())


def test_aprobacion_content_type_invalido():
    async def _run() -> None:
        headers = {
            "Idempotency-Key": "approv-2",
            "Content-Type": "text/plain",
        }
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/fe/aprobacioncomercial/api/ecf",
                content="hola",
                headers=headers,
            )
        assert response.status_code == 415

    asyncio.run(_run())
