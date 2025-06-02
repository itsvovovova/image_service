from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

from fastapi import Depends, FastAPI
from typing_extensions import Annotated

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
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "postgres"
    database_url: str = "postgresql://postgres:postgres@localhost:5432/postgres"

    # Приложение
    app_host: str = "0.0.0.0"
    app_port: int = 8007

    # Режим работы
    debug: bool = False
    log_level: str = "INFO"

    # JWT
    jwt_secret_key: str = "SECRET_KEY"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    # Модель
    model_config = SettingsConfigDict(env_file="../.env")

@lru_cache
def get_settings() -> Settings:
    return Settings()



