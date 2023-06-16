from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "feed__subreddit" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL
);
COMMENT ON TABLE "feed__subreddit" IS 'Subreddit';
CREATE TABLE IF NOT EXISTS "feed__post" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" TEXT NOT NULL,
    "author" VARCHAR(8) NOT NULL,
    "link" TEXT,
    "content" TEXT,
    "score" INT NOT NULL  DEFAULT 0,
    "promoted" BOOL NOT NULL  DEFAULT False,
    "nsfw" BOOL NOT NULL  DEFAULT False,
    "subreddit_id" INT NOT NULL REFERENCES "feed__subreddit" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "feed__post" IS 'Post';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
