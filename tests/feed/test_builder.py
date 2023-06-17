import pytest
from _pytest.monkeypatch import MonkeyPatch

from core.settings import SETTINGS
from feed import builder, models, test_data_generator
from feed.schemas import BasePost


@pytest.mark.anyio
async def test_promotion_integration_without_nsfw():
    await test_data_generator.create_test_data(100, 3, 0)
    feed: list[BasePost] = await builder.BaseBuilder().get_feed()
    assert len(feed) <= SETTINGS.FEED.PAGE_SIZE and all(
        feed[pos - 1].promoted for pos in SETTINGS.FEED.PROMOTION_POS_LIST
    )


@pytest.mark.anyio
async def test_promotion_integration_with_nsfw(subreddit: models.Subreddit):
    await models.Post.all().delete()
    await models.Post.bulk_create(
        [
            models.Post(
                title="_",
                author=f"{SETTINGS.FEED.AUTHOR_PREFIX}_t",
                subreddit_id=subreddit.pk,
                content="_",
                score=score,
                promoted=score in range(SETTINGS.FEED.PAGE_SIZE)[slice(-(len(SETTINGS.FEED.PROMOTION_POS_LIST)), None)],
                nsfw=score not in SETTINGS.FEED.PROMOTION_POS_LIST,
            )
            for score in range(1, SETTINGS.FEED.PAGE_SIZE + 1)
        ]
    )
    feed: list[BasePost] = await builder.BaseBuilder().get_feed()
    assert len(feed) <= SETTINGS.FEED.PAGE_SIZE and not any(
        feed[pos - 1].promoted for pos in SETTINGS.FEED.PROMOTION_POS_LIST
    )


@pytest.mark.anyio
async def test_promotion_integration_min_length(subreddit: models.Subreddit):
    for pos in SETTINGS.FEED.PROMOTION_POS_LIST:
        await models.Post.all().delete()
        await models.Post.bulk_create(
            [
                models.Post(
                    title="_",
                    author=f"{SETTINGS.FEED.AUTHOR_PREFIX}_t",
                    subreddit_id=subreddit.pk,
                    content="_",
                    score=0,
                    promoted=True,
                )
                for _ in range(len(SETTINGS.FEED.PROMOTION_POS_LIST))
            ]
        )
        await models.Post.bulk_create(
            [
                models.Post(
                    title="_",
                    author=f"{SETTINGS.FEED.AUTHOR_PREFIX}_t",
                    subreddit_id=subreddit.pk,
                    content="_",
                    score=score,
                )
                for score in range(1, pos + 1)
            ]
        )
        feed: list[BasePost] = await builder.BaseBuilder().get_feed()
        assert feed[pos - 1].promoted


@pytest.mark.anyio
async def test_promotion_integration_with_shift(subreddit: models.Subreddit, monkeypatch: MonkeyPatch):
    monkeypatch.setattr("core.settings.SETTINGS.FEED.SHIFT_ON", True)
    for count_integrated, pos in enumerate(SETTINGS.FEED.PROMOTION_POS_LIST):
        await models.Post.all().delete()
        await models.Post.bulk_create(
            [
                models.Post(
                    title="_",
                    author=f"{SETTINGS.FEED.AUTHOR_PREFIX}_t",
                    subreddit_id=subreddit.pk,
                    content="_",
                    score=score,
                    nsfw=ind == pos,
                    promoted=score in range(1, len(SETTINGS.FEED.PROMOTION_POS_LIST) + 1),
                )
                for ind, score in enumerate(range(1, SETTINGS.FEED.PAGE_SIZE + 1)[::-1], start=1)
            ]
        )
        feed: list[BasePost] = await builder.BaseBuilder().get_feed()
        assert feed[pos - 1 + count_integrated].nsfw and feed[pos - 1 + count_integrated + 2].promoted
