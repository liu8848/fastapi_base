from typing import Generic, Type,Iterable
from sqlalchemy import inspect,select
from sqlalchemy.ext.asyncio import AsyncSession

from common.crud.types import *
from common.crud.errors import *

class CRUDBase(Generic[Model]):
    def __init__(self, model: Type[Model]) -> None:
        self.model = model
        self.primary_key=self._get_primary_key()

    def _get_primary_key(self):
        """
        动态获取model的主键列primary_key
        """
        mapper=inspect(self.model)
        primary_key = mapper.primary_key

        if len(primary_key)==1:
            return primary_key[0]
        else:
            raise CompositePrimaryKeysError('暂不支持复合主键！')

    async def create_model(
            self,
            session: AsyncSession,
            obj: CreateSchema,
            flush: bool=False,
            commit: bool=False,
            **kwargs,
    )->Model:
        """
        创建数据实例
        @param session: SQLAlchemy 异步事物管理器
        @param obj: 包含保存数据的pydantic数据模式
        @param flush: 为True时，将所有对象变化保存到数据库，默认为false
        @param commit: 为True时，提交所有事物，默认为False
        @param kwargs: 额外的参数
        @return:
        """
        if not kwargs:
            ins=self.model(**obj.model_dump())
        else:
            ins=self.model(**obj.model_dump(),**kwargs)
        session.add(ins)
        if flush:
            await session.flush()
        if commit:
            await session.commit()
        return ins


    async def create_models(
            self,
            session: AsyncSession,
            objs: Iterable[CreateSchema],
            flush: bool=False,
            commit: bool=False,
            **kwargs,
    )->list[Model]:
        """
        批量创建数据实例
        @param session:
        @param objs:
        @param flush:
        @param commit:
        @param kwargs:
        @return:
        """
        ins_list = []
        for obj in objs:
            if not kwargs:
                ins=self.model(**obj.model_dump())
            else:
                ins=self.model(**obj.model_dump(),**kwargs)
            ins_list.append(ins)
        session.add_all(ins_list)
        if flush:
            await session.flush()
        if commit:
            await session.commit()
        return  ins_list

    async def select_model(self,session: AsyncSession,pk:int) -> Model|None:
        """
        通过主键查询数据
        @param session: SQLAlchemy 异步事务管理器
        @param pk: 数据表主键值
        @return:
        """
        stmt=select(self.model).where(self.primary_key==pk)
        query=await session.execute(stmt)
        return query.scalar().first()

    async def select_model_by_column(self,session: AsyncSession,**kwargs) -> Model|None:
        """
        按照列查询
        @param session:
        @param kwargs: 查询表达式
        @return:
        """
        filters=[]
        return filters







