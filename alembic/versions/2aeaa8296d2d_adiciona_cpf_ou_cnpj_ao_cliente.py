"""Adiciona CPF ou CNPJ ao cliente

Revision ID: 2aeaa8296d2d
Revises: 7738ddf17bc0
Create Date: 2026-09-19 16:56:57.603317

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2aeaa8296d2d'
down_revision = '7738ddf17bc0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "clientes",
        sa.Column(
            "cpf_cnpj",
            sa.String(length=14),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column(
        "clientes",
        "cpf_cnpj",
    )
