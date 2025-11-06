# FILE: tests/test_enfc_endpoints.py
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
EXPIRED_CERT_PEM = Path("tests/assets/certs/expired.pem").read_bytes()

@pytest.fixture(autouse=True)
async def _clear_idempotency():
    await idempotency_store.clear()
    yield
    await idempotency_store.clear()


@pytest.mark.asyncio
async def test_semilla_returns_seed():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/fe/autenticacion/api/semilla")
    data = response.json()
    assert response.status_code == 200
    assert "semilla" in data
    assert data["expiraEn"] == 300


@pytest.mark.asyncio
async def test_validacion_certificado_input_vacio():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/fe/autenticacion/api/validacioncertificado",
            json={},
        )
    assert response.status_code == 200
    assert response.json()["valido"] is False


@pytest.mark.asyncio
async def test_validacion_certificado_expired():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/fe/autenticacion/api/validacioncertificado",
            json={"cert_b64": base64.b64encode(EXPIRED_CERT_PEM).decode()},
        )
    assert response.status_code == 200
    assert response.json()["valido"] is False
    assert "Certificado vencido" in response.json()["detalle"]


@pytest.mark.asyncio
async def test_recepcion_ecf_requires_idempotency_header():
    payload = {
        "formato": "XML",
        "ecf_xml_b64": base64.b64encode(ECF_SAMPLE).decode(),
    }
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/fe/recepcion/api/ecf", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_recepcion_ecf_success(monkeypatch):
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


@pytest.mark.asyncio
async def test_recepcion_ecf_invalid_signature(monkeypatch):
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


@pytest.mark.asyncio
async def test_aprobacion_ecf_success(monkeypatch):
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


@pytest.mark.asyncio
async def test_aprobacion_content_type_invalido():
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
