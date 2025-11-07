import pytest
import respx
from httpx import Response
from app.dgii.client import DGIIClient

BASE_URL = "https://test.dgii.gov.do/api"

@pytest.mark.asyncio
@respx.mock
async def test_dgii_client_get_semilla():
    """
    Tests that the DGIIClient can successfully retrieve a semilla.
    """
    respx.get(f"{BASE_URL}/semilla").mock(return_value=Response(200, json={"semilla": "test-semilla"}))

    client = DGIIClient(BASE_URL, "test-id", "test-secret")
    semilla = await client.get_semilla()

    assert semilla == "test-semilla"

@pytest.mark.asyncio
@respx.mock
async def test_dgii_client_get_token():
    """
    Tests that the DGIIClient can successfully retrieve a token.
    """
    respx.post(f"{BASE_URL}/token").mock(return_value=Response(200, json={"token": "test-token"}))

    client = DGIIClient(BASE_URL, "test-id", "test-secret")
    token = await client.get_token("test-semilla")

    assert token == "test-token"
    assert client.token == "test-token"

@pytest.mark.asyncio
@respx.mock
async def test_dgii_client_send_ecf():
    """
    Tests that the DGIIClient can successfully send an e-CF.
    """
    respx.post(f"{BASE_URL}/ecf").mock(return_value=Response(200, json={"track_id": "test-track-id"}))

    client = DGIIClient(BASE_URL, "test-id", "test-secret")
    client.token = "test-token"  # Manually set the token for this test

    track_id = await client.send_ecf("<xml>test</xml>")

    assert track_id == "test-track-id"

@pytest.mark.asyncio
async def test_dgii_client_send_ecf_no_token():
    """
    Tests that the DGIIClient raises an exception when trying to send an e-CF without a token.
    """
    client = DGIIClient(BASE_URL, "test-id", "test-secret")

    with pytest.raises(Exception, match="Authentication token not available"):
        await client.send_ecf("<xml>test</xml>")
