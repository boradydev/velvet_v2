from dataclasses import dataclass

from src.core.enums import AppEnv
from src.core.settings.environ import env_field


@dataclass(frozen=True, slots=True)
class AppSettings:
    APP_ENV: AppEnv = env_field(AppEnv, "APP_ENV")
    ROOT_PATH: str = env_field(str, "ROOT_PATH")
    REGISTRATION_EXPIRE_MINUTES: int = env_field(int, "REGISTRATION_EXPIRE_MINUTES")
    CONFIRM_CODE_EXPIRE_MINUTES: int = env_field(int, "CONFIRM_CODE_EXPIRE_MINUTES")

    @property
    def debug(self) -> bool:
        return self.APP_ENV == AppEnv.dev
