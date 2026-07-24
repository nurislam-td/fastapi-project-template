from functools import lru_cache

from shared.settings.base import CoreSettings, Settings
from shared.settings.dev import DevSettings
from shared.settings.local import LocalSettings
from shared.settings.prod import ProdSettings

__all__ = ["get_settings"]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    core_settings = CoreSettings()  # pyright: ignore[reportCallIssue]
    match core_settings.ENV:
        case "dev":
            return DevSettings()  # pyright: ignore[reportCallIssue]
        case "prod":
            return ProdSettings()  # pyright: ignore[reportCallIssue]
        case _:
            return LocalSettings()  # pyright: ignore[reportCallIssue]
