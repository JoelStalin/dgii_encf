"""Generación de reportes de facturación para el portal administrativo."""
from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import List

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.billing import UsageRecord
from app.models.tenant import Tenant


def _month_range(month: datetime) -> tuple[datetime, datetime]:
    start = month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if start.month == 12:
        end = start.replace(year=start.year + 1, month=1)
    else:
        end = start.replace(month=start.month + 1)
    return start, end


def billing_summary(db: Session, month: datetime) -> List[dict]:
    """Retorna métricas agrupadas por tenant para el periodo solicitado."""

    start, end = _month_range(month)
    stmt = (
        select(
            Tenant.id.label("tenant_id"),
            Tenant.name.label("tenant_name"),
            func.count(UsageRecord.id).label("invoice_count"),
            func.coalesce(func.sum(UsageRecord.monto_cargado), 0).label("total_amount"),
        )
        .join(Tenant, Tenant.id == UsageRecord.tenant_id)
        .where(UsageRecord.fecha >= start, UsageRecord.fecha < end)
        .group_by(Tenant.id, Tenant.name)
        .order_by(Tenant.name)
    )

    results = db.execute(stmt).all()
    payload: List[dict] = []
    for row in results:
        payload.append(
            {
                "client_id": row.tenant_id,
                "client_name": row.tenant_name,
                "invoice_count": int(row.invoice_count or 0),
                "total_amount_due": Decimal(str(row.total_amount or Decimal("0"))),
            }
        )
    return payload
