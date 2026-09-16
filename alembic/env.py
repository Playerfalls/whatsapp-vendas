from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Importa as configurações da aplicação para obter a URL do banco a
# partir do .env, em vez de deixá-la fixa (e versionada) no alembic.ini.
from app.config import settings

# Objeto de configuração do Alembic, que dá acesso aos valores do alembic.ini
config = context.config

# Sobrescreve a URL do banco definida no alembic.ini com a URL montada
# dinamicamente a partir das variáveis de ambiente (.env).
config.set_main_option("sqlalchemy.url", settings.database_url)

# Configuração de logging via alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# target_metadata é usado pelo Alembic para detectar mudanças
# automaticamente (autogenerate). Permanece None nesta fase, pois ainda
# não existem models. Será definido no início da Fase 1, importando o
# Base declarativo dos models (ex: target_metadata = Base.metadata).
target_metadata = None


def run_migrations_offline() -> None:
    """Executa as migrations em modo 'offline' (gera SQL sem conectar ao banco)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Executa as migrations em modo 'online' (conecta diretamente ao banco)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
