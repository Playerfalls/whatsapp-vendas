"""Cria tabela de conversa do WhatsApp

Revision ID: f4d1d100790e
Revises: 144bbb570240
Create Date: 2026-09-18 17:57:29.167408

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4d1d100790e'
down_revision = '144bbb570240'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "conversa_whatsapp",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("telefone", sa.String(length=20), nullable=False),
        sa.Column("estado", sa.String(length=50), nullable=False),
        sa.Column("pedido_id", sa.Integer(), nullable=True),
        sa.Column("ultima_interacao", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["pedido_id"],
            ["pedidos.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_conversa_whatsapp_telefone",
        "conversa_whatsapp",
        ["telefone"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_conversa_whatsapp_telefone",
        table_name="conversa_whatsapp",
    )

    op.drop_table("conversa_whatsapp")
