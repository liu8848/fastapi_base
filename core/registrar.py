from fastapi import FastAPI

from common.log import setup_logging, set_customize_logfile
from core.conf import settings
from contextlib import asynccontextmanager


@asynccontextmanager
async def register_init(app: FastAPI):
    """
    启动初始化
    :param app:
    :return:
    """
    yield


def register_app():
    app = FastAPI(
        title=settings.FASTAPI_TITLE,
        version=settings.FASTAPI_VERSION,
        description=settings.FASTAPI_DESCRIPTION,
        docs_url=settings.FASTAPI_DOCS_URL,
        redoc_url=settings.FASTAPI_REDOC_URL,
        lifespan=register_init,
    )

    # 日志配置
    register_logger()

    return app


def register_logger() -> None:
    """配置日志"""
    setup_logging()
    set_customize_logfile()
