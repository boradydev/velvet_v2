from dataclasses import dataclass

from src.core.settings.environ import env_field


@dataclass(frozen=True, slots=True)
class PostgresSettings:
    DB_HOST: str = env_field(str, "DB_HOST")
    DB_PORT: str = env_field(str, "DB_PORT")
    POSTGRES_USER: str = env_field(str, "POSTGRES_USER")
    POSTGRES_PASSWORD: str = env_field(str, "POSTGRES_PASSWORD")
    POSTGRES_DB: str = env_field(str, "POSTGRES_DB")

    @property
    def DB_URL_ASYNC(self):
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/"
            f"{self.POSTGRES_DB}"
        )

    @property
    def DB_URL_SYNC(self):
        return (
            f"postgresql+psycopg2://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/"
            f"{self.POSTGRES_DB}"
        )
