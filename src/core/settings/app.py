import os
from dataclasses import dataclass

from src.core.enums import AppEnv


@dataclass(frozen=True, slots=True)
class AppSettings:
    APP_ENV: AppEnv = AppEnv(os.environ["APP_ENV"])
    ROOT_PATH: str = os.environ["ROOT_PATH"]
    REGISTRATION_EXPIRE_MINUTES: int = os.environ["REGISTRATION_EXPIRE_MINUTES"]
    CONFIRM_CODE_EXPIRE_MINUTES: int = os.environ["CONFIRM_CODE_EXPIRE_MINUTES"]
