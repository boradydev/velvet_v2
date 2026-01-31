from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class JwtSettings(BaseSettings):
    JWT_SECRET_KEY: SecretStr
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf8", extra="ignore")


jwt_settings = JwtSettings()  # type: ignore reportCallIssue
