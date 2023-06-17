import dataclasses

from fastapi import APIRouter

from feed import router as feed_router


@dataclasses.dataclass
class AppRouter:
    v1: tuple[APIRouter, ...] = (
        feed_router.subreddit_router,
        feed_router.post_router,
        feed_router.reddit_feed_router,
        feed_router.test_router,
    )

    @classmethod
    @property
    def routers(cls) -> tuple[tuple[str, tuple[APIRouter, ...]], ...]:
        return tuple(
            [
                (f"/api/{f_name}", f_obj.default)
                for f_name, f_obj in cls.__dataclass_fields__.items()
                if not f_name.startswith("_")
            ]
        )
