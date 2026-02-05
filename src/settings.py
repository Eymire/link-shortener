from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='APP_',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    environment: Literal['development', 'production'] = 'development'
    root_path: str | None = None
    link_length: int = 8
    link_lifetime_days: int = 30


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='DB_',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    host: str
    name: str
    user: str
    password: str


app_settings = AppSettings()  # type: ignore[call-arg]
db_settings = DatabaseSettings()  # type: ignore[call-arg]
