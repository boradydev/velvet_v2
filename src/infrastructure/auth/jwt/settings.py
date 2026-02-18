from dataclasses import dataclass

from src.core.settings.environ import env_field


@dataclass(frozen=True, slots=True)
class JwtSettings:
    JWT_SECRET_KEY: str = env_field(str, "JWT_SECRET_KEY")
    JWT_ALGORITHM: str = env_field(str, "JWT_ALGORITHM")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = env_field(
        int,
        "JWT_ACCESS_TOKEN_EXPIRE_MINUTES",
    )
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = env_field(
        int,
        "JWT_REFRESH_TOKEN_EXPIRE_DAYS",
    )
