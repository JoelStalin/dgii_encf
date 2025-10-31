"""Add accounting tables and invoice flags"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20240509_0002"
down_revision = "20240507_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("invoices", sa.Column("contabilizado", sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column("invoices", sa.Column("accounted_at", sa.DateTime(), nullable=True))
    op.add_column("invoices", sa.Column("asiento_referencia", sa.String(length=64), nullable=True))

    op.create_table(
        "tenant_settings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("tenant_id", sa.Integer(), sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False),
        sa.Column("moneda", sa.String(length=5), nullable=False, server_default="DOP"),
        sa.Column("cuenta_ingresos", sa.String(length=64), nullable=True),
        sa.Column("cuenta_itbis", sa.String(length=64), nullable=True),
        sa.Column("cuenta_retenciones", sa.String(length=64), nullable=True),
        sa.Column("dias_credito", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("correo_facturacion", sa.String(length=255), nullable=True),
        sa.Column("telefono_contacto", sa.String(length=25), nullable=True),
        sa.Column("notas", sa.String(length=512), nullable=True),
        sa.UniqueConstraint("tenant_id", name="uq_tenant_settings_tenant"),
    )

    op.create_table(
        "invoice_ledger_entries",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("tenant_id", sa.Integer(), sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False),
        sa.Column("invoice_id", sa.Integer(), sa.ForeignKey("invoices.id", ondelete="SET NULL"), nullable=True),
        sa.Column("referencia", sa.String(length=64), nullable=False),
        sa.Column("cuenta", sa.String(length=64), nullable=False),
        sa.Column("descripcion", sa.String(length=255), nullable=True),
        sa.Column("debit", sa.Numeric(16, 2), nullable=False, server_default="0"),
        sa.Column("credit", sa.Numeric(16, 2), nullable=False, server_default="0"),
        sa.Column("fecha", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_invoice_ledger_entries_tenant", "invoice_ledger_entries", ["tenant_id"])

def downgrade() -> None:
    op.drop_index("ix_invoice_ledger_entries_tenant", table_name="invoice_ledger_entries")
    op.drop_table("invoice_ledger_entries")
    op.drop_table("tenant_settings")
    op.drop_column("invoices", "asiento_referencia")
    op.drop_column("invoices", "accounted_at")
    op.drop_column("invoices", "contabilizado")
