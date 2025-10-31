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

ensure_poetry() {
  if command -v poetry >/dev/null 2>&1; then
    return
  fi

  info "Poetry no encontrado; intentando instalación local con pip."
  if ! python3 -m pip install --user --upgrade poetry; then
    fail "No fue posible instalar Poetry automáticamente. Instálalo manualmente y vuelve a ejecutar este script."
  fi

  local user_bin="${HOME}/.local/bin"
  if [ -d "$user_bin" ] && ! command -v poetry >/dev/null 2>&1; then
    export PATH="$user_bin:$PATH"
    hash -r 2>/dev/null || true
  fi

  command -v poetry >/dev/null 2>&1 || fail "Se requiere el comando 'poetry' pero no se encontró en PATH incluso después de intentar instalarlo."
}

info "Verificando dependencias del sistema"
require_cmd python3
ensure_poetry

python3 <<'PY'
import sys

REQUIRED = (3, 12)
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
