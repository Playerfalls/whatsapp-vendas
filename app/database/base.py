from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Classe base declarativa do SQLAlchemy 2.0.

    Todos os models (app/models/*.py) herdam desta classe. O Alembic usa
    `Base.metadata` (importado em alembic/env.py) para saber quais tabelas
    existem e gerar as migrations.
    """

    pass
