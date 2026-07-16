from functools import lru_cache

from shared.settings.base import CoreSettings, Settings
from shared.settings.dev import DevSettings
from shared.settings.local import LocalSettings
from shared.settings.prod import ProdSettings

__all__ = ["get_settings"]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    core_settings = CoreSettings()  # type: ignore
    match core_settings.ENV:
        case "dev":
            return DevSettings()  # type: ignore
        case "prod":
            return ProdSettings()  # type: ignore
        case _:
            return LocalSettings()  # type: ignore
