"""Esquemas Pydantic para panel administrativo."""
from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field


class TenantSettingsPayload(BaseModel):
    moneda: str = Field(default="DOP", max_length=5)
    cuenta_ingresos: Optional[str] = Field(default=None, max_length=64)
    cuenta_itbis: Optional[str] = Field(default=None, max_length=64)
    cuenta_retenciones: Optional[str] = Field(default=None, max_length=64)
    dias_credito: int = Field(default=0, ge=0, le=365)
    correo_facturacion: Optional[str] = Field(default=None, max_length=255)
    telefono_contacto: Optional[str] = Field(default=None, max_length=25)
    notas: Optional[str] = Field(default=None, max_length=512)


class TenantSettingsResponse(TenantSettingsPayload):
    updated_at: datetime


class LedgerEntryBase(BaseModel):
    referencia: str = Field(..., max_length=64)
    cuenta: str = Field(..., max_length=64)
    descripcion: Optional[str] = Field(default=None, max_length=255)
    debit: Decimal = Field(default=Decimal("0"), ge=Decimal("0"))
    credit: Decimal = Field(default=Decimal("0"), ge=Decimal("0"))
    fecha: datetime = Field(default_factory=datetime.utcnow)


class LedgerEntryCreate(LedgerEntryBase):
    invoice_id: Optional[int] = None


class LedgerEntryItem(LedgerEntryBase):
    id: int
    invoice_id: Optional[int]
    encf: Optional[str]

    class Config:
        from_attributes = True


class LedgerPaginatedResponse(BaseModel):
    items: List[LedgerEntryItem]
    total: int
    page: int
    size: int


class LedgerStatusBreakdown(BaseModel):
    contabilizados: int
    pendientes: int


class LedgerTotals(BaseModel):
    total_emitidos: int
    total_aceptados: int
    total_rechazados: int
    total_monto: Decimal


class LedgerMonthlyStat(BaseModel):
    periodo: str
    cantidad: int
    monto: Decimal


class LedgerSummaryResponse(BaseModel):
    totales: LedgerTotals
    contabilidad: LedgerStatusBreakdown
    series: List[LedgerMonthlyStat]


class PlanBase(BaseModel):
    name: str = Field(..., max_length=120)
    precio_mensual: Decimal = Field(default=Decimal("0"), ge=Decimal("0"))
    precio_por_documento: Decimal = Field(default=Decimal("0"), ge=Decimal("0"))
    documentos_incluidos: int = Field(default=0, ge=0)
    descripcion: Optional[str] = Field(default=None, max_length=255)


class PlanCreate(PlanBase):
    pass


class PlanUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=120)
    precio_mensual: Optional[Decimal] = Field(default=None, ge=Decimal("0"))
    precio_por_documento: Optional[Decimal] = Field(default=None, ge=Decimal("0"))
    documentos_incluidos: Optional[int] = Field(default=None, ge=0)
    descripcion: Optional[str] = Field(default=None, max_length=255)


class PlanResponse(PlanBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TenantPlanAssignment(BaseModel):
    plan_id: Optional[int] = Field(default=None, ge=1)


class BillingSummaryItem(BaseModel):
    client_id: int
    client_name: str
    invoice_count: int
    total_amount_due: Decimal


class BillingSummaryResponse(BaseModel):
    month: str
    generated_at: datetime
    items: List[BillingSummaryItem]
    total_amount_due: Decimal


class TenantPlanResponse(BaseModel):
    tenant_id: int
    plan: Optional[PlanResponse] = None
