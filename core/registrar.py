from contextlib import asynccontextmanager

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI

from common.exception.exception_handler import register_exception
from common.log import set_customize_logfile, setup_logging
from core.conf import settings
from database.db_mysql import create_table


@asynccontextmanager
async def register_init(app: FastAPI):
    """
    启动初始化
    :param app:
    :return:
    """
    # 创建数据库表
    await create_table()

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
    # register_logger()

    # 配置中间件
    register_middleware(app)

    # 路由
    register_router(app)

    # 异常处理
    register_exception(app)

    return app


def register_logger() -> None:
    """配置日志"""
    setup_logging()
    set_customize_logfile()


def register_middleware(app: FastAPI):
    """
    中间件执行顺序，从下到上
    :param app:
    :return:
    """
    # Trace ID (required) 生成http请求唯一id
    app.add_middleware(CorrelationIdMiddleware, validator=False)

    # 添加跨域处理中间件(要保持在最下层)
    if settings.MIDDLEWARE_CORS:
        from fastapi.middleware.cors import CORSMiddleware

        app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
            # expose_headers=settings.CORS_EXPOSE_HEADERS,
        )


def register_router(app: FastAPI):
    """
    路由配置
    """
    from app.router import router as app_router

    app.include_router(app_router)
