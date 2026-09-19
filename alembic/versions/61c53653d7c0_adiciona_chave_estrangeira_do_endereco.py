"""Adiciona chave estrangeira do endereco

Revision ID: 61c53653d7c0
Revises: 1d4faf5afac4
Create Date: 2026-09-19 12:58:29.939852

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61c53653d7c0'
down_revision = '1d4faf5afac4'
branch_labels = None
depends_on = None


def upgrade() -> None:
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
