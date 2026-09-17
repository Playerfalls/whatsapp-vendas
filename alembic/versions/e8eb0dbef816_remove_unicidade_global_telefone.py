"""remove unicidade global de clientes.telefone (fase 4)

A unicidade de telefone passa a ser garantida na camada de service,
considerando apenas clientes ativos - ver app/services/cliente_service.py
e o comentário no model Cliente.

Revision ID: e8eb0dbef816
Revises: 27e1178a903d
Create Date: 2026-09-18 00:00:00.000000

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "e8eb0dbef816"
down_revision = "27e1178a903d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_constraint("uq_clientes_telefone", "clientes", type_="unique")
    op.create_index("ix_clientes_telefone", "clientes", ["telefone"])


def downgrade() -> None:
    op.drop_index("ix_clientes_telefone", table_name="clientes")
    op.create_unique_constraint("uq_clientes_telefone", "clientes", ["telefone"])
