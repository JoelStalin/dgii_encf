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

prompt() {
  local message="$1"
  local default="${2:-Y}"
  local response
  printf '%s [%s]: ' "$message" "$default"
  read -r response
  if [ -z "$response" ]; then
    response="$default"
  fi
  printf '%s' "$response"
}

ensure_pip() {
  if python3 -m pip --version >/dev/null 2>&1; then
    return
  fi

  info "Python se encuentra instalado pero no se detectó el módulo 'pip'."
  if command -v apt-get >/dev/null 2>&1; then
    local answer
    answer="$(prompt "¿Deseas instalar python3-pip usando apt-get? Requiere privilegios de sudo" "Y")"
    case "${answer^^}" in
      Y|YES)
        if ! (sudo apt-get update && sudo apt-get install -y python3-pip); then
          fail "No fue posible instalar pip mediante apt-get."
        fi
        ;;
      *)
        fail "pip es requerido para completar la instalación. Instálalo manualmente e intenta de nuevo."
        ;;
    esac
  else
    fail "pip es requerido y no se puede instalar automáticamente en este entorno."
  fi
}

require_cmd() {
  local cmd="$1"
  command -v "$cmd" >/dev/null 2>&1 || fail "Se requiere el comando '$cmd' pero no se encontró en PATH."
}

ensure_poetry() {
  if command -v poetry >/dev/null 2>&1; then
    return
  fi

  ensure_pip
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

# Permite personalizar grupos opcionales via POETRY_INSTALL_GROUPS (por defecto "dev").
POETRY_INSTALL_GROUPS=${POETRY_INSTALL_GROUPS:-dev}
poetry_install_args=(install)
if [ -n "$POETRY_INSTALL_GROUPS" ]; then
  poetry_install_args+=(--with "$POETRY_INSTALL_GROUPS")
fi

if ! poetry "${poetry_install_args[@]}"; then
  info "Poetry reportó un problema al instalar dependencias; intentando regenerar poetry.lock"
  lock_args=(lock)
  if poetry lock --help 2>&1 | grep -q -- "--no-update"; then
    lock_args+=(--no-update)
  fi

  if ! poetry "${lock_args[@]}" >/dev/null 2>&1; then
    info "Fallo 'poetry ${lock_args[*]}'; intentando 'poetry lock' completo"
    poetry lock || fail "No se pudo regenerar poetry.lock automáticamente."
  fi
  poetry "${poetry_install_args[@]}" || fail "'poetry install' continuó fallando incluso luego de regenerar poetry.lock."
fi

info "Instalación completada. Activa el entorno con 'poetry shell' o utiliza 'poetry run <comando>'."
