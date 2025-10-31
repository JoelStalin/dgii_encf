"""Global fixtures for DGII tests."""
from __future__ import annotations

import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Generator, Tuple

import pytest
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.x509.oid import NameOID

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture(scope="session")
def certificate_bundle(tmp_path_factory: pytest.TempPathFactory) -> Tuple[Path, bytes, rsa.RSAPrivateKey, x509.Certificate]:
    cert_dir = tmp_path_factory.mktemp("certs")
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = issuer = x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, "DO"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Test Company"),
            x509.NameAttribute(NameOID.COMMON_NAME, "test.getupnet.local"),
        ]
    )
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.utcnow() - timedelta(days=1))
        .not_valid_after(datetime.utcnow() + timedelta(days=365))
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        .sign(key, hashes.SHA256())
    )

    password = b"testpass"
    p12_bytes = pkcs12.serialize_key_and_certificates(
        name=b"test",
        key=key,
        cert=cert,
        cas=None,
        encryption_algorithm=serialization.BestAvailableEncryption(password),
    )
    output_path = cert_dir / "test_cert.p12"
    output_path.write_bytes(p12_bytes)
    return output_path, password, key, cert


@pytest.fixture
def configured_settings(certificate_bundle: Tuple[Path, bytes, rsa.RSAPrivateKey, x509.Certificate]):
    from app.core.config import settings

    path, password, _key, cert = certificate_bundle
    original_path = settings.dgii_cert_p12_path
    original_password = settings.dgii_cert_p12_password
    settings.dgii_cert_p12_path = path
    settings.dgii_cert_p12_password = password.decode()
    try:
        yield {
            "path": path,
            "password": password,
            "certificate": cert,
        }
    finally:
        settings.dgii_cert_p12_path = original_path
        settings.dgii_cert_p12_password = original_password
