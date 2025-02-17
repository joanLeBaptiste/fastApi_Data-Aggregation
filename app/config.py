from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "local")
    DATABASE_URL_LOCAL: str = os.getenv("DATABASE_URL_LOCAL")
    DATABASE_URL_DOCKER: str = os.getenv("DATABASE_URL_DOCKER")

    @property
    def DATABASE_URL(self):
        return self.DATABASE_URL_DOCKER if self.ENVIRONMENT == "docker" else self.DATABASE_URL_LOCAL

    class Config:
        env_file = ".env"

settings = Settings()
