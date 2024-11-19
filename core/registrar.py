from fastapi import FastAPI,Depends
from asgi_correlation_id import CorrelationIdMiddleware
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

    # 配置中间件
    # register_middleware(app)

    # 路由
    register_router(app)

    return app


def register_logger() -> None:
    """配置日志"""
    setup_logging()
    set_customize_logfile()


def register_middleware(app: FastAPI):
    """
    中间件执行顺序，从上到下
    :param app:
    :return:
    """
    # Trace ID (required) 生成http请求唯一id
    app.add_middleware(CorrelationIdMiddleware, validator=False)


def register_router(app: FastAPI):
    """
    路由配置
    """
    from app.router import router as app_router
    app.include_router(app_router)
