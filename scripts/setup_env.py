"""Asistente interactivo para configurar el entorno de desarrollo."""
from __future__ import annotations

import os
from pathlib import Path

TEMPLATE = Path(".env.example")
TARGET = Path(".env.development")


def main() -> None:
    if not TEMPLATE.exists():
        raise SystemExit("No se encontró .env.example")
    if TARGET.exists():
        print(".env.development ya existe, no se sobrescribirá.")
        return
    data = TEMPLATE.read_text(encoding="utf-8")
    TARGET.write_text(data, encoding="utf-8")
    print("Archivo .env.development generado. Recuerde actualizar credenciales sensibles.")


if __name__ == "__main__":
    main()
