"""Cria cobranca pix

Revision ID: 7738ddf17bc0
Revises: 282ff56f05c2
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7738ddf17bc0"
down_revision = "282ff56f05c2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "cobrancas_pix",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "pagamento_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "asaas_payment_id",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "pix_payload",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "pix_expira_em",
            sa.DateTime(),
            nullable=False,
        ),
        sa.Column(
            "status_externo",
            sa.String(length=50),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["pagamento_id"],
            ["pagamentos.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("asaas_payment_id"),
        sa.UniqueConstraint("pagamento_id"),
    )

    op.create_index(
        "ix_cobrancas_pix_asaas_payment_id",
        "cobrancas_pix",
        ["asaas_payment_id"],
        unique=True,
    )

    op.create_index(
        "ix_cobrancas_pix_pagamento_id",
        "cobrancas_pix",
        ["pagamento_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_cobrancas_pix_pagamento_id",
        table_name="cobrancas_pix",
    )

    op.drop_index(
        "ix_cobrancas_pix_asaas_payment_id",
        table_name="cobrancas_pix",
    )

    op.drop_table("cobrancas_pix")