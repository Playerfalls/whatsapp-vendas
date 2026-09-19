from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configurações da aplicação, carregadas a partir do arquivo .env.

    Nesta fase (Fase 0), contém apenas o necessário para conectar ao banco
    de dados. Novas variáveis (WhatsApp, pagamento, autenticação etc.)
    serão adicionadas somente quando as respectivas fases forem
    implementadas - não antecipamos configuração que ainda não é usada.
    """

    # Banco de dados
    db_user: str
    db_password: str
    db_host: str = "localhost"
    db_port: int = 3306
    db_name: str
    
        # Asaas
    asaas_api_key: str
    asaas_base_url: str = "https://api-sandbox.asaas.com/v3"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def database_url(self) -> str:
        """Monta a URL de conexão do SQLAlchemy para o MySQL usando o driver PyMySQL."""
        return (
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()
