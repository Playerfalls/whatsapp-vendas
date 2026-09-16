from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

# Engine do SQLAlchemy: gerencia o pool de conexões com o MySQL.
# pool_pre_ping evita erros de "conexão perdida" em conexões ociosas.
engine = create_engine(settings.database_url, pool_pre_ping=True)

# Fábrica de sessões: cada requisição usará sua própria sessão, criada
# a partir desta fábrica.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Dependência do FastAPI para obter uma sessão de banco de dados por
    requisição, garantindo que a sessão seja sempre fechada ao final.

    Uso futuro (a partir da Fase 1, quando existirem rotas de negócio):

        @router.get("/produtos")
        def listar_produtos(db: Session = Depends(get_db)):
            ...

    Nesta fase (Fase 0) esta função ainda não é utilizada por nenhuma
    rota - existe apenas como infraestrutura pronta para as próximas fases.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
