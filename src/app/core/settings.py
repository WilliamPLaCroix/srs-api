from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central configuration for the application.
    Values are loaded from environment variables first,
    then fallback defaults.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # App metadata
    service_name: str = "app"

    # Database
    database_url: str = "sqlite:///./app.db"

    # Runtime
    environment: str = "development"  # development | staging | production

    # API
    api_prefix: str = ""


settings = Settings()