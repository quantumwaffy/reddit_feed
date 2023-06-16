from typing import TypeVar

from pydantic import BaseSettings

from . import mixins

TortoiseConfig = TypeVar("TortoiseConfig", bound=dict)


class AppSettings(mixins.EnvSettingsMixin):
    """Basic app settings

    Attrs:
        DEBUG: Debug mode
    """

    DEBUG: bool


class TortoiseORMSettings(mixins.EnvSettingsMixin):
    """Tortoise ORM settings using PostgreSQL

    Attrs:
        POSTGRES_USER: Postgres DB user
        POSTGRES_PASSWORD: Postgres DB password
        POSTGRES_DB: Postgres DB name
        POSTGRES_HOST: Postgres DB host
        POSTGRES_PORT: Postgres DB port
        DB_TIMEZONE: Postgres DB timezone
    """

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    DB_TIMEZONE: str = "Europe/Warsaw"

    def _get_config(self, db_url: str) -> TortoiseConfig:
        return {
            "connections": {"default": db_url},
            "apps": {
                "models": {
                    "models": ["aerich.models", "feed.models"],
                    "default_connection": "default",
                },
            },
            "timezone": f"{self.DB_TIMEZONE}",
        }

    @property
    def url(self) -> str:
        return (
            f"postgres://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def config(self) -> TortoiseConfig:
        return self._get_config(self.url)

    @property
    def test_config(self) -> TortoiseConfig:
        return self._get_config("sqlite://:memory:")


class Settings(BaseSettings):
    APP: AppSettings = AppSettings()
    ORM: TortoiseORMSettings = TortoiseORMSettings()


SETTINGS: Settings = Settings()
