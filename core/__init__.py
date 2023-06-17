from tortoise import Tortoise

Tortoise.init_models(
    ["feed.models"],
    "models",
)
