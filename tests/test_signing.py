from pathlib import Path
from app.dgii.signing import XMLSigningService, verify_xml_signature
from signxml import SignatureMethod
from cryptography import x509
from cryptography.hazmat.primitives.serialization import pkcs12, Encoding

TEST_P12_PATH = Path(__file__).parent / "test_cert.p12"
TEST_P12_PASSWORD = "testpassword"

def test_xml_signing_service():
    """
    Tests that the XMLSigningService can sign an XML document.
    """
    service = XMLSigningService(TEST_P12_PATH, TEST_P12_PASSWORD)
    xml_content = b"<root><data>Hello, World!</data></root>"
    signed_xml = service.sign_xml(xml_content)

    # Extract the certificate from the P12 file for verification
    with open(TEST_P12_PATH, "rb") as f:
        p12 = pkcs12.load_key_and_certificates(f.read(), TEST_P12_PASSWORD.encode())
    cert = p12[1].public_bytes(Encoding.PEM)

    assert b"Signature" in signed_xml
    assert SignatureMethod.RSA_SHA256.value.encode() in signed_xml
    assert verify_xml_signature(signed_xml, cert) is True

def test_verify_xml_signature_invalid():
    """
    Tests that the verify_xml_signature function returns False for an invalid signature.
    """
    xml_content = b"<root><data>Hello, World!</data></root>"

    # Use a dummy certificate for verification
    with open(TEST_P12_PATH, "rb") as f:
        p12 = pkcs12.load_key_and_certificates(f.read(), TEST_P12_PASSWORD.encode())
    cert = p12[1].public_bytes(Encoding.PEM)

    assert verify_xml_signature(xml_content, cert) is False
