from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from .settings import SETTINGS


def get_app() -> FastAPI:
    api: FastAPI = FastAPI(
        debug=SETTINGS.APP.DEBUG,
        swagger_ui_parameters={"persistAuthorization": True},
        **{"docs_url": None, "redoc_url": None} if not SETTINGS.APP.DEBUG else {}
    )
    return api


def _init_app():
    api: FastAPI = get_app()
    register_tortoise(
        api,
        config=SETTINGS.ORM.config,
        generate_schemas=True,
        add_exception_handlers=True,
    )
    return api


app: FastAPI = _init_app()
