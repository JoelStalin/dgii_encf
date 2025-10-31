"""Add indexes for invoices"""

from __future__ import annotations

from alembic import op

revision = "20240510_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index("ix_invoices_encf", "invoices", ["encf"], unique=True)
    op.create_index("ix_invoices_rnc", "invoices", ["rnc_emisor"])
    op.create_index("ix_invoices_estado", "invoices", ["estado_dgii"])


def downgrade() -> None:
    op.drop_index("ix_invoices_estado", table_name="invoices")
    op.drop_index("ix_invoices_rnc", table_name="invoices")
    op.drop_index("ix_invoices_encf", table_name="invoices")
