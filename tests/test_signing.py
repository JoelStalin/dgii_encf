from __future__ import annotations

from typing import Generator

import pytest
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.x509.oid import NameOID
from datetime import datetime, timedelta
from signxml import XMLVerifier

from app.security.signing import sign_xml_enveloped
from app.security.xml import parse_secure


@pytest.fixture(scope="module")
def temporary_p12(tmp_path_factory: pytest.TempPathFactory) -> Generator[tuple[str, str], None, None]:
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    name = x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, "DO"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "DGII Test"),
            x509.NameAttribute(NameOID.COMMON_NAME, "dgii.example"),
        ]
    )
    cert = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.utcnow())
        .not_valid_after(datetime.utcnow() + timedelta(days=365))
        .sign(key, hashes.SHA256())
    )
    password = "pass"
    p12_bytes = pkcs12.serialize_key_and_certificates(
        name=b"dgii",
        key=key,
        cert=cert,
        cas=None,
        encryption_algorithm=serialization.BestAvailableEncryption(password.encode()),
    )
    path = tmp_path_factory.mktemp("certs") / "test.p12"
    path.write_bytes(p12_bytes)
    yield str(path), password


def test_sign_xml_enveloped(temporary_p12: tuple[str, str]) -> None:
    xml = b'<?xml version="1.0" encoding="UTF-8"?><eCF><Encabezado/></eCF>'
    signed = sign_xml_enveloped(xml, temporary_p12[0], temporary_p12[1])
    root = parse_secure(signed)
    signature = root.find(".//{http://www.w3.org/2000/09/xmldsig#}Signature")
    assert signature is not None
    XMLVerifier().verify(signed)
