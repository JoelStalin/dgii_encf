#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

info() {
  printf '==> %s\n' "$1"
}

fail() {
  printf 'Error: %s\n' "$1" >&2
  exit 1
}

require_cmd() {
  local cmd="$1"
  command -v "$cmd" >/dev/null 2>&1 || fail "Se requiere el comando '$cmd' pero no se encontró en PATH."
}

info "Verificando dependencias del sistema"
require_cmd python3
require_cmd poetry

python3 <<'PY'
import sys

REQUIRED = (3, 11)
if sys.version_info < REQUIRED:
    version = ".".join(map(str, sys.version_info[:3]))
    required = ".".join(map(str, REQUIRED))
    raise SystemExit(f"Python {required}+ es requerido, se encontró {version}.")
PY

info "Creando archivo .env.development si no existe"
if [ -f ".env.example" ]; then
  python3 scripts/setup_env.py
else
  info "No se encontró .env.example; omitiendo generación automática."
fi

info "Instalando dependencias vía Poetry"
poetry install

info "Instalación completada. Activa el entorno con 'poetry shell' o utiliza 'poetry run <comando>'."
