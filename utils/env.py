from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Secrets
    JWT_SECRET: str

    # Config
    JWT_COOKIE_EXPIRE_MINUTES: int = 60

    # Environment
    ENVIRONMENT: str = "development"

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )

env = Settings()