from typing import Literal
from urllib.parse import quote

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_TYPE = Literal["dev", "prod", "local"]
LOG_LEVEL_TYPE = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class CoreSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    # APP ENV
    ENV: ENV_TYPE
    LOG_LEVEL: LOG_LEVEL_TYPE = "ERROR"


class Settings(CoreSettings):
    # APP ENV
    APP_NAME: str = "app"

    # database
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        password = quote(self.DB_PASSWORD, safe="")
        return f"postgresql+asyncpg://{self.DB_USER}:{password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def SYNC_DATABASE_URL(self) -> str:
        password = quote(self.DB_PASSWORD, safe="")
        return f"postgresql://{self.DB_USER}:{password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # openapi
    API_PREFIX: str = f"/{APP_NAME}/api"
    WS_PREFIX: str = f"/{APP_NAME}/ws"
    DOCS_URL: str = API_PREFIX + "/docs/"
    OPENAPI_URL: str = f"{API_PREFIX}/openapi.json"

    # DEPLOY
    API_HOST: str = "localhost"
    API_PORT: int = 8080
    API_WORKERS: int = 1
    API_RELOAD: bool = False
