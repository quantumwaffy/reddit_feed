from fastapi import APIRouter, HTTPException, status

from . import builder, models, schemas, test_data_generator, utils

subreddit_router: APIRouter = APIRouter(
    prefix="/subreddit",
    tags=["Subreddit of Posts"],
)

post_router: APIRouter = APIRouter(
    prefix="/post",
    tags=["Post from Feed"],
)

reddit_feed_router: APIRouter = APIRouter(
    prefix="/feed",
    tags=["Reddit Feed"],
)

test_router: APIRouter = APIRouter(
    prefix="/test",
    tags=["Test data generator"],
)


@subreddit_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_subreddit(subreddit_data: schemas.NewSubredditInput) -> schemas.NewSubredditOutput:
    if await utils.subreddit_exists(name=subreddit_data.name):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "The specified Subreddit already exists")
    subreddit_obj: models.Subreddit = await models.Subreddit.create(**subreddit_data.dict())
    return await schemas.NewSubredditOutput.from_tortoise_orm(subreddit_obj)


@post_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_post(post_data: schemas.PostInput) -> schemas.BasePost:
    if not await utils.subreddit_exists(id=post_data.subreddit_id):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "The specified Subreddit does not exist")
    post_obj: models.Post = await models.Post.create(**post_data.dict())
    return await schemas.BasePost.from_tortoise_orm(post_obj)


@test_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_test_data(init_data: schemas.TestDataInput) -> schemas.TestDataLog:
    created_data: dict[str, int] = await test_data_generator.create_test_data(**init_data.dict())
    return schemas.TestDataLog(**created_data)


@reddit_feed_router.get("/", status_code=status.HTTP_200_OK)
async def get_feed(page: int = 1) -> list[schemas.BasePost]:
    return await builder.BaseBuilder(page_num=page).get_feed()
