from typing import Unpack

from . import models


async def subreddit_exists(**kwargs: Unpack[dict[str, str | int]]) -> bool:
    return await models.Subreddit.filter(**kwargs).exists()
