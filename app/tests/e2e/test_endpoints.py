"""Pruebas integradas básicas."""
from __future__ import annotations

import base64

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_healthz() -> None:
    response = client.get("/healthz")
    assert response.status_code == 200


def test_sign_and_dgii_flow() -> None:
    xml = base64.b64encode(b"<Factura><Total>1</Total></Factura>").decode()
    sign_resp = client.post("/api/1/sign/xml", json={"xml": xml, "certificate_subject": "CN=Demo"})
    assert sign_resp.status_code == 200
    codigo = sign_resp.json()["codigo_seguridad"]
    dgii_resp = client.post("/api/1/dgii/rfce/send", json={"encf": "E310000000001", "resumen_xml": "<r/>"})
    assert dgii_resp.status_code == 200
    assert len(codigo) == 6
