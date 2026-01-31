from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.enums import AppEnv


class Settings(BaseSettings):
    APP_ENV: AppEnv
    APP_HOST: str
    ROOT_PATH: str
    UNCONFIRMED_REGISTRATION_EXPIRE_MINUTES: int
    CONFIRM_CODE_EXPIRE_MINUTES: int
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf8", extra="ignore")


settings = Settings()  # type: ignore reportCallIssue
