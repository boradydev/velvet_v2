import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class JwtSettings:
    JWT_SECRET_KEY: str = os.environ["JWT_SECRET_KEY"]
    JWT_ALGORITHM: str = os.environ["JWT_ALGORITHM"]
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.environ["JWT_ACCESS_TOKEN_EXPIRE_MINUTES"]
    )
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = int(
        os.environ["JWT_REFRESH_TOKEN_EXPIRE_DAYS"]
    )
