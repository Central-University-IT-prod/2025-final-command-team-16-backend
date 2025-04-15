from pathlib import Path
from typing import Literal

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class PostgresConfig(BaseModel):
    username: str
    password: str
    host: str
    port: int
    database: str
    echo: bool = False
    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    @property
    def url_with_driver(self) -> str:
        return f"postgresql+asyncpg://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"


class RedisConfig(BaseModel):
    host: str
    port: int
    database: int


class MailConfig(BaseModel):
    username: str
    password: str
    from_email: str
    port: int
    server: str
    from_name: str


class ServerConfig(BaseModel):
    url: str
    host: str
    port: int
    cookie_max_age_minutes: int = 3600
    reset_password_token: str
    verification_token: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=BASE_DIR / ".env",
        env_nested_delimiter="__",
        extra="ignore",
    )
    server: ServerConfig
    mail: MailConfig
    postgres: PostgresConfig
    redis: RedisConfig
    mode: Literal["prod", "debug", "test"] = "prod"
    upload_dir: str = "uploads"


settings = Settings()
