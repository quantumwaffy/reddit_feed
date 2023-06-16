from tortoise import fields

from core import base as core_base


class Subreddit(core_base.BaseModel):
    name = fields.CharField(max_length=50)

    class Meta:
        table_description = "Subreddit"

    def __str__(self) -> str:
        return f"{self.__class__.__name__} '{self.name}'"

    class PydanticMeta:
        exclude = ("id",)


class Post(core_base.BaseModel):
    title = fields.TextField()
    author = fields.CharField(max_length=8)
    link = fields.TextField(null=True)
    subreddit = fields.ForeignKeyField("models.Subreddit", related_name="posts")
    content = fields.TextField(null=True)
    score = fields.IntField(default=0)
    promoted = fields.BooleanField(default=False)
    nsfw = fields.BooleanField(default=False)

    class Meta:
        table_description = "Post"
        ordering = ["-score"]

    def __str__(self) -> str:
        return f"{self.__class__.__name__} #{self.pk}"

    class PydanticMeta:
        exclude = ("id",)
