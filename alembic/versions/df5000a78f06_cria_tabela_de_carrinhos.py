"""Cria tabela de carrinhos

Revision ID: df5000a78f06
Revises: f4d1d100790e
Create Date: 2026-09-18 23:51:45.091351

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df5000a78f06'
down_revision = 'f4d1d100790e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "carrinhos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("conversa_id", sa.Integer(), nullable=False),
        sa.Column("criado_em", sa.DateTime(), nullable=False),
        sa.Column("atualizado_em", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["conversa_id"],
            ["conversa_whatsapp.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_carrinhos_conversa_id",
        "carrinhos",
        ["conversa_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_carrinhos_conversa_id",
        table_name="carrinhos",
    )
    op.drop_table("carrinhos")