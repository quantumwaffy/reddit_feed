import abc
from typing import Type

from tortoise.queryset import QuerySet

from core.settings import SETTINGS, FeedSettings

from . import models, schemas


class AbstractBuilder(abc.ABC):
    _model: "Type[models.Post]" = models.Post
    _output_schema: "Type[schemas.BasePost]" = schemas.BasePost
    _feed_settings: FeedSettings = SETTINGS.FEED

    def __init__(self, page_num: int = 1) -> None:
        self._page_num: int = page_num

    def _get_first_ind(self, size: int) -> int:
        return 0 if self._page_num == 1 else self._page_num * size - size

    async def _get_page_promotions(self) -> list[_model]:
        qs: QuerySet = self._get_page_promotions_qs()
        max_promotions_count: int = len(self._feed_settings.PROMOTION_POS_LIST)
        return await qs.offset(self._get_first_ind(max_promotions_count)).limit(max_promotions_count) or await qs.limit(
            max_promotions_count
        )

    async def _get_page_posts(self) -> list[_model]:
        qs: QuerySet = self._get_page_posts_qs()
        page_size_with_buffer: int = self._feed_settings.PAGE_SIZE - len(self._feed_settings.PROMOTION_POS_LIST)
        return await qs.offset(self._get_first_ind(page_size_with_buffer)).limit(page_size_with_buffer)

    async def _serialize_feed(self, feed: list[_model]) -> list[_output_schema]:
        return [await self._output_schema.from_tortoise_orm(post) for post in feed]

    async def get_feed(self) -> list[_output_schema]:
        feed: list[models.Post] = await self._get_page_posts()

        for promotion_post, promotion_ind in zip(
            await self._get_page_promotions(), self._feed_settings.PROMOTION_POS_LIST
        ):
            self._check_and_insert(promotion_post, promotion_ind - 1, feed)
        return await self._serialize_feed(feed)

    def _check_and_insert(self, promotion_post: models.Post, promotion_ind: int, feed: list[models.Post]) -> None:
        if promotion_ind >= len(feed):
            return
        if not tuple(filter(lambda post: post.nsfw, feed[promotion_ind - 1 : promotion_ind + 2])):
            feed.insert(promotion_ind, promotion_post)
        elif self._feed_settings.SHIFT_ON:
            self._check_and_insert(promotion_post, promotion_ind + 1, feed)

    @abc.abstractmethod
    def _get_page_promotions_qs(self) -> QuerySet:
        ...

    @abc.abstractmethod
    def _get_page_posts_qs(self) -> QuerySet:
        ...


class BaseBuilder(AbstractBuilder):
    def _get_page_promotions_qs(self) -> QuerySet:
        return self._model.filter(promoted=True).order_by("id")

    def _get_page_posts_qs(self) -> QuerySet:
        return self._model.filter(promoted=False)
