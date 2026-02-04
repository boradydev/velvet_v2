from src.core.enums import AppEnv
from src.core.settings.base import Settings


class AppSettings(Settings):
    APP_ENV: AppEnv
    APP_HOST: str
    ROOT_PATH: str
    UNCONFIRMED_REGISTRATION_EXPIRE_MINUTES: int
    CONFIRM_CODE_EXPIRE_MINUTES: int


settings = AppSettings()  # type: ignore reportCallIssue
