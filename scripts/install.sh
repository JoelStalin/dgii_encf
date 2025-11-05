#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "
${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR" || exit 1

log() { printf "\033[1;36m[install]\033[0m %s\n" "$*"; }
err() { printf "\033[1;31m[err]\033[0m %s\n" "$*" >&2; }

log "==> Preparando dependencias del sistema"
if [ -f "scripts/system_deps.sh" ]; then
  bash scripts/system_deps.sh
else
  err "scripts/system_deps.sh no existe. Aborta."
  exit 1
fi

export PATH="$HOME/.local/bin:$PATH"

if ! command -v python3 >/dev/null 2>&1; then
  err "python3 no disponible."
  exit 1
fi

if ! command -v pipx >/dev/null 2>&1; then
  err "pipx no disponible tras ejecutar system_deps.sh."
  exit 1
fi

pipx ensurepath || true
export PATH="$HOME/.local/bin:$PATH"

if command -v poetry >/dev/null 2>&1; then
  log "Poetry detectado. Intentando actualización..."
  pipx upgrade poetry || log "No fue posible actualizar Poetry (continuando)."
else
  log "Instalando Poetry mediante pipx..."
  if ! pipx install poetry; then
    err "No se pudo instalar Poetry con pipx."
    # continuamos para que la verificación siguiente falle de forma clara si no está instalado
  fi
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

if [ -f "pyproject.toml" ] && [ "$USE_PIP_FALLBACK" != "1" ]; then
  log "==> Instalando dependencias con Poetry"
  poetry --version >/dev/null 2>&1 || { err "Poetry no disponible tras la instalación."; exit 1; }
  poetry install --no-interaction --no-ansi
else
  log "==> Modo fallback: entorno virtual + pip"
  python3 -m venv .venv
  # shellcheck disable=SC1091
  source .venv/bin/activate
  python -m pip install --upgrade pip
  if [ -f "scripts/python_deps.txt" ]; then
    python -m pip install -r scripts/python_deps.txt
  else
    err "scripts/python_deps.txt no existe."
    exit 1
  fi
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

log "Resumen: $PYV | $POEV | pipx $PXV"
log "Instalación completada."