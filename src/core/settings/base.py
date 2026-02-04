from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.paths import PROJECT_DIR


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(PROJECT_DIR / ".env"),
        env_file_encoding="utf8",
        extra="ignore",
    )
