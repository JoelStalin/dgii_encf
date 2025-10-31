"""Endpoints administrativos para contabilidad y configuración de empresas."""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.admin.schemas import (
    LedgerEntryCreate,
    LedgerEntryItem,
    LedgerPaginatedResponse,
    LedgerSummaryResponse,
    LedgerTotals,
    LedgerMonthlyStat,
    LedgerStatusBreakdown,
    TenantSettingsPayload,
    TenantSettingsResponse,
)
from app.models.accounting import InvoiceLedgerEntry, TenantSettings
from app.models.invoice import Invoice
from app.models.tenant import Tenant
from app.shared.database import get_db


router = APIRouter(prefix="/admin", tags=["Admin"])


def _get_tenant_or_404(db: Session, tenant_id: int) -> Tenant:
    tenant = db.get(Tenant, tenant_id)
    if not tenant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant no encontrado")
    return tenant


def _get_settings(db: Session, tenant_id: int) -> TenantSettings:
    settings = db.scalar(select(TenantSettings).where(TenantSettings.tenant_id == tenant_id))
    if settings:
        return settings
    settings = TenantSettings(tenant_id=tenant_id)
    db.add(settings)
    db.flush()
    return settings


@router.get("/tenants/{tenant_id}/accounting/summary", response_model=LedgerSummaryResponse)
def get_accounting_summary(tenant_id: int, db: Session = Depends(get_db)) -> LedgerSummaryResponse:
    _get_tenant_or_404(db, tenant_id)

    total_emitidos = db.scalar(select(func.count()).where(Invoice.tenant_id == tenant_id)) or 0
    total_aceptados = db.scalar(select(func.count()).where(Invoice.tenant_id == tenant_id, Invoice.estado_dgii == "ACEPTADO")) or 0
    total_rechazados = db.scalar(select(func.count()).where(Invoice.tenant_id == tenant_id, Invoice.estado_dgii == "RECHAZADO")) or 0
    total_monto = db.scalar(select(func.coalesce(func.sum(Invoice.total), 0)).where(Invoice.tenant_id == tenant_id)) or Decimal("0")

    contabilizados = db.scalar(select(func.count()).where(Invoice.tenant_id == tenant_id, Invoice.contabilizado.is_(True))) or 0

    series_data: dict[str, dict[str, Decimal | int]] = defaultdict(lambda: {"monto": Decimal("0"), "cantidad": 0})
    rows = db.execute(select(Invoice.fecha_emision, Invoice.total).where(Invoice.tenant_id == tenant_id)).all()
    for fecha_emision, total in rows:
        if not fecha_emision:
            continue
        periodo = fecha_emision.strftime("%Y-%m")
        bucket = series_data[periodo]
        bucket["cantidad"] = int(bucket["cantidad"]) + 1
        bucket["monto"] = bucket["monto"] + Decimal(str(total))

    series = [
        LedgerMonthlyStat(periodo=periodo, cantidad=bucket["cantidad"], monto=bucket["monto"])
        for periodo, bucket in sorted(series_data.items())
    ]

    return LedgerSummaryResponse(
        totales=LedgerTotals(
            total_emitidos=total_emitidos,
            total_aceptados=total_aceptados,
            total_rechazados=total_rechazados,
            total_monto=Decimal(str(total_monto)),
        ),
        contabilidad=LedgerStatusBreakdown(
            contabilizados=contabilizados,
            pendientes=max(total_emitidos - contabilizados, 0),
        ),
        series=series,
    )


@router.get("/tenants/{tenant_id}/accounting/ledger", response_model=LedgerPaginatedResponse)
def list_ledger_entries(
    tenant_id: int,
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    contabilizado: Optional[bool] = Query(None),
) -> LedgerPaginatedResponse:
    _get_tenant_or_404(db, tenant_id)

    base_query = (
        select(InvoiceLedgerEntry, Invoice)
        .join(Invoice, InvoiceLedgerEntry.invoice_id == Invoice.id, isouter=True)
        .where(InvoiceLedgerEntry.tenant_id == tenant_id)
    )

    if contabilizado is not None:
        base_query = base_query.where(Invoice.contabilizado.is_(contabilizado))

    total = db.scalar(select(func.count()).select_from(base_query.subquery())) or 0

    stmt = (
        base_query.order_by(InvoiceLedgerEntry.fecha.desc())
        .offset((page - 1) * size)
        .limit(size)
    )

    entries = db.execute(stmt).all()

    items: list[LedgerEntryItem] = []
    for entry, invoice in entries:
        items.append(
            LedgerEntryItem(
                id=entry.id,
                invoice_id=entry.invoice_id,
                encf=invoice.encf if invoice else None,
                referencia=entry.referencia,
                cuenta=entry.cuenta,
                descripcion=entry.descripcion,
                debit=Decimal(str(entry.debit)),
                credit=Decimal(str(entry.credit)),
                fecha=entry.fecha,
            )
        )

    return LedgerPaginatedResponse(items=items, total=total, page=page, size=size)


@router.post("/tenants/{tenant_id}/accounting/ledger", response_model=LedgerEntryItem, status_code=status.HTTP_201_CREATED)
def create_ledger_entry(
    tenant_id: int,
    payload: LedgerEntryCreate,
    db: Session = Depends(get_db),
) -> LedgerEntryItem:
    _get_tenant_or_404(db, tenant_id)

    invoice: Optional[Invoice] = None
    if payload.invoice_id is not None:
        invoice = db.get(Invoice, payload.invoice_id)
        if not invoice or invoice.tenant_id != tenant_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comprobante no encontrado")

    entry = InvoiceLedgerEntry(
        tenant_id=tenant_id,
        invoice_id=payload.invoice_id,
        referencia=payload.referencia,
        cuenta=payload.cuenta,
        descripcion=payload.descripcion,
        debit=payload.debit,
        credit=payload.credit,
        fecha=payload.fecha,
    )
    db.add(entry)

    if invoice:
        invoice.contabilizado = True
        invoice.accounted_at = payload.fecha
        invoice.asiento_referencia = payload.referencia

    db.flush()

    return LedgerEntryItem(
        id=entry.id,
        invoice_id=entry.invoice_id,
        encf=invoice.encf if invoice else None,
        referencia=entry.referencia,
        cuenta=entry.cuenta,
        descripcion=entry.descripcion,
        debit=Decimal(str(entry.debit)),
        credit=Decimal(str(entry.credit)),
        fecha=entry.fecha,
    )


@router.get("/tenants/{tenant_id}/settings", response_model=TenantSettingsResponse)
def get_tenant_settings(tenant_id: int, db: Session = Depends(get_db)) -> TenantSettingsResponse:
    _get_tenant_or_404(db, tenant_id)
    settings = _get_settings(db, tenant_id)
    return TenantSettingsResponse(
        moneda=settings.moneda,
        cuenta_ingresos=settings.cuenta_ingresos,
        cuenta_itbis=settings.cuenta_itbis,
        cuenta_retenciones=settings.cuenta_retenciones,
        dias_credito=settings.dias_credito,
        correo_facturacion=settings.correo_facturacion,
        telefono_contacto=settings.telefono_contacto,
        notas=settings.notas,
        updated_at=settings.updated_at,
    )


@router.put("/tenants/{tenant_id}/settings", response_model=TenantSettingsResponse)
def update_tenant_settings(
    tenant_id: int,
    payload: TenantSettingsPayload,
    db: Session = Depends(get_db),
) -> TenantSettingsResponse:
    _get_tenant_or_404(db, tenant_id)
    settings = _get_settings(db, tenant_id)

    for field, value in payload.model_dump().items():
        setattr(settings, field, value)

    db.flush()

    return TenantSettingsResponse(
        moneda=settings.moneda,
        cuenta_ingresos=settings.cuenta_ingresos,
        cuenta_itbis=settings.cuenta_itbis,
        cuenta_retenciones=settings.cuenta_retenciones,
        dias_credito=settings.dias_credito,
        correo_facturacion=settings.correo_facturacion,
        telefono_contacto=settings.telefono_contacto,
        notas=settings.notas,
        updated_at=settings.updated_at,
    )
