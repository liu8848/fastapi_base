import sys

from typing import Annotated
from uuid import uuid4

from fastapi import Depends
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession,async_sessionmaker

from common.model import MappedBase
from core.conf import settings
from common.log import log

def create_engine_and_mission(url :str | URL):
    try:
        # 创建数据库引擎
        engine= create_async_engine(url,echo=settings.MYSQL_ECHO,future=True,pool_pre_ping=True)
    except Exception as e:
        log.error('数据库连接失败 {}',e)
        sys.exit()
    else:
        db_session=async_sessionmaker(bind=engine,autoflush=False,expire_on_commit=False)
        log.info('数据库连接成功')
        return engine,db_session

SQLALCHEMY_DATABASE_URL = (
    f'mysql+asyncmy://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOST}:'
    f'{settings.MYSQL_PORT}/{settings.MYSQL_DATABASE}?charset={settings.MYSQL_CHARSET}'
)

async_engine,async_db_session=create_engine_and_mission(SQLALCHEMY_DATABASE_URL)

async def get_db()->AsyncSession:
    """session生成器"""
    session=async_db_session()
    try:
        yield session
    except Exception as se:
        await session.rollback()
        raise se
    finally:
        await session.close()

CurrentSession=Annotated[AsyncSession,Depends(get_db)]

async def create_table():
    """创建数据库"""
    async with async_engine.begin() as conn:
        await conn.run_sync(MappedBase.metadata.create_all)


def uuid4_str() -> str:
    """数据库引擎 UUID 类型兼容性解决方案"""
    return str(uuid4())