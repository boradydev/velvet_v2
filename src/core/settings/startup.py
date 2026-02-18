from dataclasses import dataclass

from src.core.settings.environ import env_field


@dataclass(frozen=True, slots=True)
class StartupSettings:
    ENTRY_POINT: str = env_field(str, "ENTRY_POINT")
    APP_HOST: str = env_field(str, "APP_HOST")
    APP_PORT: int = env_field(int, "APP_PORT")
