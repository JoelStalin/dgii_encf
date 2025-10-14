"""Cifra .env.production utilizando AES-256-GCM."""
from __future__ import annotations

import argparse
import os
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def encrypt_env(input_path: Path, output_path: Path, key: bytes) -> None:
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    data = input_path.read_bytes()
    encrypted = nonce + aesgcm.encrypt(nonce, data, None)
    output_path.write_bytes(encrypted)


def main() -> None:
    parser = argparse.ArgumentParser(description="Cifra archivos .env usando AES-256-GCM")
    parser.add_argument("--input", default=".env.production", type=Path)
    parser.add_argument("--output", default=".env.production.enc", type=Path)
    parser.add_argument("--key", help="Clave hexadecimal de 32 bytes")
    args = parser.parse_args()

    key = bytes.fromhex(args.key) if args.key else AESGCM.generate_key(bit_length=256)
    encrypt_env(args.input, args.output, key)
    if not args.key:
        print("KEY_HEX=", key.hex())


if __name__ == "__main__":
    main()
