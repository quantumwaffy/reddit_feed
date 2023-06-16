import random
from operator import itemgetter
from uuid import uuid4

from tortoise.transactions import in_transaction

from . import models
from .consts import PostKindCounts


async def create_test_data(post_count: int, promoted_percent: int, nsfw_percent: int) -> dict[str, int]:
    init_data: dict[str, int] = {
        PostKindCounts.PROMOTION: int(post_count * promoted_percent / 100),
        PostKindCounts.NSFW: int(post_count * nsfw_percent / 100),
    }
    init_data |= {
        PostKindCounts.BASIC: post_count - init_data[PostKindCounts.PROMOTION] - init_data[PostKindCounts.NSFW]
    }
    async with in_transaction():
        for kind, count in filter(itemgetter(1), init_data.items()):
            subreddit: models.Subreddit = await models.Subreddit.create(name=f"subreddit_{kind}_{uuid4().hex}")
            await models.Post.bulk_create(
                [
                    models.Post(
                        title=f"{kind}_title_{i}",
                        author=f"t2_{kind}{i}",
                        subreddit=subreddit,
                        content=f"{kind}_content_{i}",
                        score=random.randint(-100, 100),
                        promoted=kind == PostKindCounts.PROMOTION,
                        nsfw=kind == PostKindCounts.NSFW,
                    )
                    for i in range(1, count + 1)
                ]
            )
    return init_data
