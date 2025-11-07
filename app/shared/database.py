"""Gestión de la conexión a la base de datos PostgreSQL."""
from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from sqlalchemy.orm import Session

from app.db import SyncSessionFactory


@contextmanager
def session_scope() -> Iterator[Session]:
    """Provee un contexto seguro para operaciones DB reutilizando el engine async."""

    session = SyncSessionFactory()
    try:
        yield session
        session.commit()
    except Exception:  # pragma: no cover - defensive rollback
        session.rollback()
        raise
    finally:
        session.close()


def get_db() -> Iterator[Session]:
    """Dependencia de FastAPI para inyectar sesiones transaccionales."""

    with session_scope() as session:
        yield session
