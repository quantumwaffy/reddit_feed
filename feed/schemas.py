import validators
from pydantic import BaseModel, Field, root_validator, validator
from tortoise.contrib.pydantic import pydantic_model_creator

from core.settings import SETTINGS

from . import consts, models

BasePost = pydantic_model_creator(models.Post, name="BasePost")
BasePostInput = pydantic_model_creator(models.Post, name="BasePostInput", exclude=("subreddit", "id"))

BaseSubreddit = pydantic_model_creator(models.Subreddit, name="BaseSubreddit")
NewSubredditInput = pydantic_model_creator(models.Subreddit, name="NewSubredditInput", exclude=("posts", "id"))
NewSubredditOutput = pydantic_model_creator(models.Subreddit, name="NewSubredditOutput", exclude=("posts",))


class PostInput(BasePostInput):
    author: str = Field(regex=rf"^{SETTINGS.FEED.AUTHOR_PREFIX}[a-z0-9]+$")
    subreddit_id: int

    @validator("link")
    def validate_link(cls, link: str) -> str:
        if link and not validators.url(link):
            raise ValueError("Must contain valid URL")
        return link

    @root_validator()
    def validate_content_and_link(cls, values: dict[str, str | int | bool]) -> dict[str, str | int | bool]:
        link: str = values.get("link")
        text: str = values.get("content")
        if link and text or not link and not text:
            raise ValueError("Provide 'link' or 'content'")
        return values


class TestDataInput(BaseModel):
    post_count: int = Field(
        150,
        ge=SETTINGS.FEED.PAGE_SIZE,
        le=250,
        title="Count of posts",
        description="Count of posts of all kinds to create",
    )
    promoted_percent: int = Field(
        40,
        ge=10,
        le=50,
        title="Promoted posts percentage",
        description="The percentage of promoted posts from the total count",
    )
    nsfw_percent: int = Field(
        10,
        ge=5,
        le=20,
        title="NSFW posts percentage",
        description="The percentage of NSFW posts from the total count",
    )


class TestDataLog(BaseModel):
    promoted_count: int = Field(
        ...,
        alias=consts.PostKindCounts.PROMOTION.value,
        title="Promoted posts count",
        description="Created count of promoted posts",
    )
    nsfw_count: int = Field(
        ...,
        alias=consts.PostKindCounts.NSFW.value,
        title="NSFW posts count",
        description="Created count of NSFW posts",
    )
    basic_content_count: int = Field(
        ...,
        alias=consts.PostKindCounts.BASIC.value,
        title="Standard posts count",
        description="Created count of standard posts",
    )
