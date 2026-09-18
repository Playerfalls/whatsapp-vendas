"""Cria configuracao de automacao

Revision ID: 144bbb570240
Revises: e8eb0dbef816
Create Date: 2026-09-18 17:10:51.359977

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '144bbb570240'
down_revision = 'e8eb0dbef816'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "configuracao_automacao",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("ativa", sa.Boolean(), nullable=False),
        sa.Column("data_atualizacao", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("configuracao_automacao")
