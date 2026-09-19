"""Adiciona endereco temporario a conversa

Revision ID: 1d4faf5afac4
Revises: c15f682118c9
Create Date: 2026-09-19 12:50:05.869178

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d4faf5afac4'
down_revision = 'c15f682118c9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "conversa_whatsapp",
        sa.Column(
            "endereco_id",
            sa.Integer(),
            nullable=True,
        ),
    )
    op.create_foreign_key(
        None,
        "conversa_whatsapp",
        "enderecos",
        ["endereco_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        None,
        "conversa_whatsapp",
        type_="foreignkey",
    )
    op.drop_column(
        "conversa_whatsapp",
        "endereco_id",
    )
