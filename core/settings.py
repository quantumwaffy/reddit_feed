from typing import TypeVar

from pydantic import BaseSettings, root_validator, validator

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


class FeedSettings(mixins.EnvSettingsMixin):
    """Feed builder settings

    Attrs:
        PAGE_SIZE: The size of one page in the feed
        PROMOTION_POS_LIST: Positions in the feed to integrate promoted posts
        AUTHOR_PREFIX: Required prefix to the author's nickname
        SHIFT_ON: Allows to find a new place for promoted posts when it's impossible to insert it in the right position
    """

    PAGE_SIZE: int = 27
    PROMOTION_POS_LIST: list[int] = [2, 16]
    AUTHOR_PREFIX: str = "t2_"
    SHIFT_ON: bool = False

    @validator("PROMOTION_POS_LIST")
    def validate_promotion_pos_list(cls, promotion_pos_list: list) -> list[int]:
        if not promotion_pos_list:
            raise ValueError("'PROMOTION_POS_LIST' cannot be empty")
        return promotion_pos_list

    @root_validator()
    def validate_page_settings(
        cls, values: dict[str, str | list[int] | bool | int]
    ) -> dict[str, str | list[int] | bool | int]:
        if (promotion_pos_list := values.get("PROMOTION_POS_LIST")) and any(
            ind > values["PAGE_SIZE"] for ind in promotion_pos_list
        ):
            raise ValueError("The value in the 'PROMOTION_POS_LIST' cannot be greater than the value of 'PAGE_SIZE'")
        return values


class Settings(BaseSettings):
    APP: AppSettings = AppSettings()
    ORM: TortoiseORMSettings = TortoiseORMSettings()
    FEED: FeedSettings = FeedSettings()


SETTINGS: Settings = Settings()
