"""Adiciona forma de pagamento temporaria na conversa

Revision ID: 282ff56f05c2
Revises: 61c53653d7c0
Create Date: 2026-09-19 13:45:12.494152

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '282ff56f05c2'
down_revision = '61c53653d7c0'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column(
        "conversa_whatsapp",
        sa.Column(
            "forma_pagamento",
            sa.String(length=20),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column(
        "conversa_whatsapp",
        "forma_pagamento",
    )
