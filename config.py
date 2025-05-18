from pydantic import BaseSettings

class Settings(BaseSettings):
    port: int = 8007

    class Config:
        env_file = '.env'

settings = Settings()
