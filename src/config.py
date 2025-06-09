from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # RabbitMQ
    rabbitmq_user: str = "guest"
    rabbitmq_password: str = "guest"
    rabbitmq_host: str = "rabbitmq"
    rabbitmq_port: int = 5672
    rabbitmq_management_port: int = 15672

    # PostgreSQL
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_host: str = "db"
    postgres_port: int = 5432
    postgres_db: str = "image_database"
    database_url: str = (
        f"postgresql://{postgres_user}:{postgres_password}"
        f"@{postgres_host}:{postgres_port}/{postgres_db}"
    )

    # Redis
    redis_port: int = 6379

    # App
    app_host: str = "0.0.0.0"
    app_port: int = 8007

    # Work
    debug: bool = False
    log_level: str = "INFO"

    # JWT
    jwt_secret_key: str = "9f2d7a6b3e4c1d5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    model_config = SettingsConfigDict(env_file="../.env")

@lru_cache
def get_settings() -> Settings:
    return Settings()



