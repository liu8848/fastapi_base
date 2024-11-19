from typing import Literal
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from core.path_conf import BasePath


# 全局配置类
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=f'{BasePath}/.env', env_file_encoding='utf-8', extra='ignore')

    # 环境配置
    ENVIRONMENT: Literal['dev', 'pro']

    # Fast API 基础设置
    FASTAPI_API_V1_PATH: str = '/api/v1'
    FASTAPI_TITLE: str = 'FastAPI'
    FASTAPI_VERSION: str = 'v1'
    FASTAPI_DESCRIPTION: str | None = 'FastAPI'
    FASTAPI_DOCS_URL: str | None = f'{FASTAPI_API_V1_PATH}/docs'
    FASTAPI_REDOC_URL: str | None = f'{FASTAPI_API_V1_PATH}/redoc'

    # 日志配置
    LOG_ROOT_LEVEL: str = 'NOTSET'
    # LOG_STD_FORMAT: str = (
    #     '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <lvl>{level: <8}</lvl>} | '
    #     '<cyan> {correlation_id} </cyan> | <lvl>{message}</lvl>'
    # )
    # LOG_FILE_FORMAT: str = (
    #     '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</> | <lvl>{level: <8}</> | '
    #     '<cyan> {correlation_id} </> | <lvl>{message}</>'
    # )
    LOG_STD_FORMAT: str = (
        '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</> | <lvl>{level: <8}</> | '
        '<cyan> {correlation_id} </> | <lvl>{message}</>'
    )
    LOG_FILE_FORMAT: str = (
        '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</> | <lvl>{level: <8}</> | '
        '<cyan> {correlation_id} </> | <lvl>{message}</>'
    )
    LOG_CID_DEFAULT_VALUE: str = '-'
    LOG_CID_UUID_LENGTH: int = 32
    LOG_STDOUT_LEVEL: str = 'INFO'
    LOG_STDERR_LEVEL: str = 'ERROR'
    LOG_STDOUT_FILENAME: str = 'info.log'
    LOG_STDERR_FILENAME: str = 'error.log'


@lru_cache
def get_settings() -> Settings:
    return Settings()


# 创建配置实例
settings = get_settings()
