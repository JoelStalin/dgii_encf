from fastapi import APIRouter, Request, Response, Depends
from app.dgii.validation import get_validator_for
from app.dgii.client import DGIIClient
from app.core.config import settings

router = APIRouter()

def get_dgii_client():
    return DGIIClient(
        base_url=settings.DGII_BASE_URL,
        client_id=settings.DGII_CLIENT_ID,
        client_secret=settings.DGII_CLIENT_SECRET,
    )

@router.post("/arecf", status_code=202)
async def receive_arecf(request: Request):
    """
    Receives an ARECF (Acuse de Recibo de e-CF) from a client.
    """
    xml_content = await request.body()

    # 1. Validate the XML against the ARECF schema
    validator = get_validator_for("ARECF")
    if not validator.validate_xml(xml_content):
        return Response(status_code=400, content="Invalid ARECF XML")

    # 2. Parse the XML to extract relevant data
    #    (e.g., eNCF, RNCComprador, Estado, etc.)
    #    This will require an XML parsing library like lxml.

    # 3. Store the ARECF data in the database.
    #    This will require a database model and a database session.

    return {"status": "ARECF received, validated, and queued for processing"}

@router.post("/acecf", status_code=202)
async def receive_acecf(request: Request, dgii_client: DGIIClient = Depends(get_dgii_client)):
    """
    Receives an ACECF (Aprobación Comercial de e-CF) from a client.
    """
    xml_content = await request.body()

    # 1. Validate the XML against the ACECF schema
    validator = get_validator_for("ACECF")
    if not validator.validate_xml(xml_content):
        return Response(status_code=400, content="Invalid ACECF XML")

    # 2. Parse the XML to extract relevant data.

    # 3. Store the ACECF data in the database.

    # 4. Send a copy of the ACECF to the DGII.
    #    This will require the DGIIClient to have a method for sending ACECFs.
    #    await dgii_client.send_acecf(xml_content)

    return {"status": "ACECF received, validated, and queued for processing and submission to DGII"}

@router.post("/anecf", status_code=202)
async def receive_anecf(request: Request):
    """
    Receives an ANECF (Anulación de e-NCF) from a client.
    """
    xml_content = await request.body()

    # 1. Validate the XML against the ANECF schema
    validator = get_validator_for("ANECF")
    if not validator.validate_xml(xml_content):
        return Response(status_code=400, content="Invalid ANECF XML")

    # 2. Parse the XML to extract relevant data.

    # 3. Store the ANECF data in the database.

    return {"status": "ANECF received, validated, and queued for processing"}
