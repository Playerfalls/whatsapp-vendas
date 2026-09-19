"""Cria tabela de itens carrinho

Revision ID: c15f682118c9
Revises: df5000a78f06
Create Date: 2026-09-19 08:29:04.533601

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c15f682118c9'
down_revision = 'df5000a78f06'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "itens_carrinho",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("carrinho_id", sa.Integer(), nullable=False),
        sa.Column("produto_id", sa.Integer(), nullable=False),
        sa.Column("quantidade", sa.Integer(), nullable=False),
        sa.Column("preco_unitario", sa.Numeric(10, 2), nullable=False),
        sa.ForeignKeyConstraint(
            ["carrinho_id"],
            ["carrinhos.id"],
        ),
        sa.ForeignKeyConstraint(
            ["produto_id"],
            ["produtos.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_itens_carrinho_carrinho_id",
        "itens_carrinho",
        ["carrinho_id"],
        unique=False,
    )

    op.create_index(
        "ix_itens_carrinho_produto_id",
        "itens_carrinho",
        ["produto_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_itens_carrinho_produto_id",
        table_name="itens_carrinho",
    )

    op.drop_index(
        "ix_itens_carrinho_carrinho_id",
        table_name="itens_carrinho",
    )

    op.drop_table("itens_carrinho")