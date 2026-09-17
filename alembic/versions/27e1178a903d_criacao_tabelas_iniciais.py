"""criacao das tabelas iniciais (fase 1)

Revision ID: 27e1178a903d
Revises:
Create Date: 2026-09-18 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "27e1178a903d"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "cidades",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nome", sa.String(length=120), nullable=False),
        sa.Column("ativo", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_index("ix_cidades_nome", "cidades", ["nome"])

    op.create_table(
        "categorias",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nome", sa.String(length=120), nullable=False),
        sa.Column("ativo", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_index("ix_categorias_nome", "categorias", ["nome"])

    op.create_table(
        "clientes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nome", sa.String(length=150), nullable=False),
        sa.Column("telefone", sa.String(length=20), nullable=False),
        sa.Column("data_cadastro", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("ativo", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.UniqueConstraint("telefone", name="uq_clientes_telefone"),
    )

    op.create_table(
        "bairros",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("cidade_id", sa.Integer(), sa.ForeignKey("cidades.id"), nullable=False),
        sa.Column("nome", sa.String(length=120), nullable=False),
        sa.Column("valor_taxa_entrega", sa.Numeric(10, 2), nullable=False),
        sa.Column("ativo", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_index("ix_bairros_cidade_id", "bairros", ["cidade_id"])

    op.create_table(
        "produtos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("categoria_id", sa.Integer(), sa.ForeignKey("categorias.id"), nullable=False),
        sa.Column("nome", sa.String(length=150), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=True),
        sa.Column("preco", sa.Numeric(10, 2), nullable=False),
        sa.Column("quantidade_estoque", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("ativo", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_index("ix_produtos_categoria_id", "produtos", ["categoria_id"])

    op.create_table(
        "enderecos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("cliente_id", sa.Integer(), sa.ForeignKey("clientes.id"), nullable=False),
        sa.Column("bairro_id", sa.Integer(), sa.ForeignKey("bairros.id"), nullable=False),
        sa.Column("cep", sa.String(length=9), nullable=False),
        sa.Column("logradouro", sa.String(length=200), nullable=False),
        sa.Column("numero", sa.String(length=20), nullable=False),
        sa.Column("complemento", sa.String(length=200), nullable=True),
        sa.Column("ponto_referencia", sa.String(length=200), nullable=True),
        sa.Column("ativo", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_index("ix_enderecos_cliente_id", "enderecos", ["cliente_id"])
    op.create_index("ix_enderecos_bairro_id", "enderecos", ["bairro_id"])

    op.create_table(
        "pedidos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("cliente_id", sa.Integer(), sa.ForeignKey("clientes.id"), nullable=False),
        sa.Column("endereco_id", sa.Integer(), sa.ForeignKey("enderecos.id"), nullable=True),
        sa.Column("cep_entrega", sa.String(length=9), nullable=False),
        sa.Column("logradouro_entrega", sa.String(length=200), nullable=False),
        sa.Column("numero_entrega", sa.String(length=20), nullable=False),
        sa.Column("complemento_entrega", sa.String(length=200), nullable=True),
        sa.Column("ponto_referencia_entrega", sa.String(length=200), nullable=True),
        sa.Column("bairro_entrega_nome", sa.String(length=120), nullable=False),
        sa.Column("cidade_entrega_nome", sa.String(length=120), nullable=False),
        sa.Column("taxa_entrega_aplicada", sa.Numeric(10, 2), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "NOVO", "PREPARANDO", "PRONTO", "EM_ROTA", "FINALIZADO",
                "CANCELADO", "RETORNADO",
                name="status_pedido_enum", native_enum=False, length=20,
            ),
            nullable=False,
            server_default="NOVO",
        ),
        sa.Column("valor_total", sa.Numeric(10, 2), nullable=False),
        sa.Column("data_criacao", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column(
            "data_atualizacao", sa.DateTime(), server_default=sa.func.now(), nullable=False
        ),
    )
    op.create_index("ix_pedidos_cliente_id", "pedidos", ["cliente_id"])
    op.create_index("ix_pedidos_endereco_id", "pedidos", ["endereco_id"])
    op.create_index("ix_pedidos_status", "pedidos", ["status"])

    op.create_table(
        "itens_pedido",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("pedido_id", sa.Integer(), sa.ForeignKey("pedidos.id"), nullable=False),
        sa.Column("produto_id", sa.Integer(), sa.ForeignKey("produtos.id"), nullable=False),
        sa.Column("quantidade", sa.Integer(), nullable=False),
        sa.Column("preco_unitario", sa.Numeric(10, 2), nullable=False),
        sa.Column("subtotal", sa.Numeric(10, 2), nullable=False),
    )
    op.create_index("ix_itens_pedido_pedido_id", "itens_pedido", ["pedido_id"])
    op.create_index("ix_itens_pedido_produto_id", "itens_pedido", ["produto_id"])

    op.create_table(
        "pagamentos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("pedido_id", sa.Integer(), sa.ForeignKey("pedidos.id"), nullable=False),
        sa.Column(
            "forma_pagamento",
            sa.Enum(
                "DINHEIRO", "PIX", "CARTAO",
                name="forma_pagamento_enum", native_enum=False, length=20,
            ),
            nullable=False,
        ),
        sa.Column(
            "status_pagamento",
            sa.Enum(
                "PENDENTE", "PAGO", "CANCELADO",
                name="status_pagamento_enum", native_enum=False, length=20,
            ),
            nullable=False,
            server_default="PENDENTE",
        ),
        sa.Column("valor", sa.Numeric(10, 2), nullable=False),
        sa.Column("data_pagamento", sa.DateTime(), nullable=True),
        sa.UniqueConstraint("pedido_id", name="uq_pagamentos_pedido_id"),
    )

    op.create_table(
        "historico_status_pedido",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("pedido_id", sa.Integer(), sa.ForeignKey("pedidos.id"), nullable=False),
        sa.Column(
            "status_anterior",
            sa.Enum(
                "NOVO", "PREPARANDO", "PRONTO", "EM_ROTA", "FINALIZADO",
                "CANCELADO", "RETORNADO",
                name="status_pedido_enum", native_enum=False, length=20,
            ),
            nullable=True,
        ),
        sa.Column(
            "status_novo",
            sa.Enum(
                "NOVO", "PREPARANDO", "PRONTO", "EM_ROTA", "FINALIZADO",
                "CANCELADO", "RETORNADO",
                name="status_pedido_enum", native_enum=False, length=20,
            ),
            nullable=False,
        ),
        sa.Column(
            "data_alteracao", sa.DateTime(), server_default=sa.func.now(), nullable=False
        ),
    )
    op.create_index(
        "ix_historico_status_pedido_pedido_id", "historico_status_pedido", ["pedido_id"]
    )


def downgrade() -> None:
    op.drop_table("historico_status_pedido")
    op.drop_table("pagamentos")
    op.drop_table("itens_pedido")
    op.drop_table("pedidos")
    op.drop_table("enderecos")
    op.drop_table("produtos")
    op.drop_table("bairros")
    op.drop_table("clientes")
    op.drop_table("categorias")
    op.drop_table("cidades")
