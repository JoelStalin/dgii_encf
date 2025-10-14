"""Creación inicial de tablas."""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "20240507_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "tenants",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("rnc", sa.String(11), nullable=False, unique=True),
        sa.Column("env", sa.String(20)),
        sa.Column("dgii_base_ecf", sa.String(255)),
        sa.Column("dgii_base_fc", sa.String(255)),
        sa.Column("cert_ref", sa.String(255)),
        sa.Column("p12_kms_key", sa.String(255)),
    )

    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
        sa.Column("tenant_id", sa.Integer, sa.ForeignKey("tenants.id", ondelete="CASCADE")),
        sa.Column("email", sa.String(255), unique=True),
        sa.Column("phone", sa.String(20)),
        sa.Column("password_hash", sa.String(255)),
        sa.Column("mfa_secret", sa.String(32)),
        sa.Column("role", sa.String(30)),
        sa.Column("status", sa.String(20)),
    )

    op.create_table(
        "invoices",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
        sa.Column("tenant_id", sa.Integer, sa.ForeignKey("tenants.id", ondelete="CASCADE")),
        sa.Column("encf", sa.String(20)),
        sa.Column("tipo_ecf", sa.String(3)),
        sa.Column("xml_path", sa.String(255)),
        sa.Column("xml_hash", sa.String(128)),
        sa.Column("estado_dgii", sa.String(30)),
        sa.Column("track_id", sa.String(64)),
        sa.Column("codigo_seguridad", sa.String(6)),
        sa.Column("total", sa.Numeric(16, 2)),
        sa.Column("fecha_emision", sa.DateTime),
    )

    op.create_index("ix_invoices_tenant_encf", "invoices", ["tenant_id", "encf"], unique=False)

    op.create_table(
        "rfce_submissions",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
        sa.Column("tenant_id", sa.Integer, sa.ForeignKey("tenants.id", ondelete="CASCADE")),
        sa.Column("encf", sa.String(20)),
        sa.Column("resumen_xml_path", sa.String(255)),
        sa.Column("estado", sa.String(30)),
        sa.Column("mensajes", sa.String(512)),
        sa.Column("secuencia_utilizada", sa.String(20)),
    )

    op.create_table(
        "approvals",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
        sa.Column("tenant_id", sa.Integer, sa.ForeignKey("tenants.id", ondelete="CASCADE")),
        sa.Column("encf", sa.String(20)),
        sa.Column("rnc_emisor", sa.String(11)),
        sa.Column("rnc_comprador", sa.String(11)),
        sa.Column("estado", sa.String(1)),
        sa.Column("motivo", sa.String(255)),
    )

    op.create_table(
        "receipts",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
        sa.Column("tenant_id", sa.Integer, sa.ForeignKey("tenants.id", ondelete="CASCADE")),
        sa.Column("encf", sa.String(20)),
        sa.Column("rnc_emisor", sa.String(11)),
        sa.Column("rnc_comprador", sa.String(11)),
        sa.Column("estado", sa.String(1)),
        sa.Column("motivo_codigo", sa.String(2)),
    )

    op.create_table(
        "anecf",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
        sa.Column("tenant_id", sa.Integer, sa.ForeignKey("tenants.id", ondelete="CASCADE")),
        sa.Column("tipo_ecf", sa.String(3)),
        sa.Column("desde", sa.Integer),
        sa.Column("hasta", sa.Integer),
        sa.Column("cantidad", sa.Integer),
        sa.Column("xml_path", sa.String(255)),
        sa.Column("estado_envio", sa.String(20)),
    )

    op.create_table(
        "xml_store",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
        sa.Column("tenant_id", sa.Integer, sa.ForeignKey("tenants.id", ondelete="CASCADE")),
        sa.Column("encf", sa.String(20)),
        sa.Column("kind", sa.String(20)),
        sa.Column("path", sa.String(255)),
        sa.Column("sha256", sa.String(64)),
    )

    op.create_table(
        "ri_store",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
        sa.Column("tenant_id", sa.Integer, sa.ForeignKey("tenants.id", ondelete="CASCADE")),
        sa.Column("encf", sa.String(20)),
        sa.Column("pdf_path", sa.String(255)),
        sa.Column("mode", sa.String(20)),
        sa.Column("hash", sa.String(128)),
    )

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
        sa.Column("tenant_id", sa.Integer, sa.ForeignKey("tenants.id", ondelete="CASCADE")),
        sa.Column("actor", sa.String(255)),
        sa.Column("action", sa.String(100)),
        sa.Column("resource", sa.String(255)),
        sa.Column("hash_prev", sa.String(128)),
        sa.Column("hash_curr", sa.String(128)),
    )


def downgrade() -> None:
    for table in [
        "audit_logs",
        "ri_store",
        "xml_store",
        "anecf",
        "receipts",
        "approvals",
        "rfce_submissions",
        "invoices",
        "users",
        "tenants",
    ]:
        op.drop_table(table)
