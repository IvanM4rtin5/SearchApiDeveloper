from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configurações da aplicação, carregadas de variáveis de ambiente.
    """
    # Carrega as variáveis do arquivo .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Chave da API do Stack Exchange (opcional, mas recomendada para evitar throttling)
    # https://stackapps.com/apps/oauth/register
    STACKEXCHANGE_KEY: str | None = None


settings = Settings()