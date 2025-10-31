from __future__ import annotations

from pathlib import Path

from cryptography.hazmat.primitives import serialization
from lxml import etree
from signxml import XMLVerifier

from app.dgii.signing import sign_ecf


def test_sign_ecf_generates_valid_signature(configured_settings) -> None:
    sample_xml = Path("samples/ecf_valid.xml").read_bytes()
    cert_info = configured_settings
    signed_xml = sign_ecf(sample_xml, str(cert_info["path"]), cert_info["password"].decode())

    root = etree.fromstring(signed_xml)
    signature_el = root.find("{http://www.w3.org/2000/09/xmldsig#}Signature")
    assert signature_el is not None
    signature_method = signature_el.find(".//{http://www.w3.org/2000/09/xmldsig#}SignatureMethod")
    digest_method = signature_el.find(".//{http://www.w3.org/2000/09/xmldsig#}DigestMethod")
    assert signature_method is not None
    assert digest_method is not None
    assert signature_method.get("Algorithm") == "http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"
    assert digest_method.get("Algorithm") == "http://www.w3.org/2001/04/xmlenc#sha256"

    XMLVerifier().verify(
        signed_xml,
        x509_cert=cert_info["certificate"].public_bytes(serialization.Encoding.DER),
    )
