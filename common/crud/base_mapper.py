from typing import Any, Generic, Type, Iterable

from sqlalchemy import inspect,select,update,delete
from sqlalchemy.ext.asyncio import AsyncSession

from common.crud.errors import CompositePrimaryKeysError
from common.crud.types import Model,CreateSchema,UpdateSchema
from database.db_mysql import async_db_session

class BaseMapper(Generic[Model]):
    def __init__(self, model: Type[Model]):
        self.model = model
        self.primary_key=self._get_primary_key()

    def _get_primary_key(self):
        """
        获取table的主键column
        :return:
        """
        mapper=inspect(self.model)
        primary_keys=mapper.primary_key
        if len(primary_keys)==1:
            return primary_keys[0]
        else:
            raise CompositePrimaryKeysError('暂不支持复合主键！')

    async def create_model(self,
                           obj:CreateSchema,
                           flush:bool= False,
                           commit:bool= False,
                           **kwargs,
    )->Model:
        """
        创建一条数据实例
        :param session: 事务管理器
        :param obj: 插入数据
        :param flush: 是否将所有对象变化保存
        :param commit: 是否自动提交
        :param kwargs: 额外参数
        :return:
        """
        if not kwargs:
            ins=self.model(**obj.model_dump())
        else:
            ins=self.model(**obj.model_dump(),**kwargs)
        async with async_db_session.begin() as session:
            session.add(ins)
            if flush:
                await session.flush()
            if commit:
                await session.commit()
        return ins

    async def create_models(self,
                            session: AsyncSession,
                            objs:Iterable[CreateSchema],
                            flush:bool= False,
                            commit:bool= False,
                            **kwargs,
    )->list[Model]:
        """
        批量创建数据实例
        :param session:
        :param objs:
        :param flush:
        :param commit:
        :param kwargs:
        :return:
        """
        ins_list=[]
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
        return ins_list

    async def select_model_by_pk(self,session: AsyncSession,pk:Any)->Model|None:
        """
        通过主键查询数据
        :param session:
        :param pk:
        :return:
        """
        stmt=select(self.model).where(self.primary_key == pk)
        query= await session.execute(stmt)
        return query.scalars().first()

    async def update_model_by_pk(
            self,
            session: AsyncSession,
            pk:Any,
            obj:UpdateSchema|dict[str,Any],
            flush:bool= False,
            commit:bool= False,
            **kwargs,
    )->int:
        """
        根据主键更新数据
        :param session:
        :param pk:
        :param obj:
        :param flush:
        :param commit:
        :param kwargs:
        :return:
        """
        if isinstance(obj,dict):
            instance_data=obj
        else:
            instance_data=obj.model_dump(exclude_unset=True)
        stmt=update(self.model).where(self.primary_key == pk).values(**instance_data)
        result = await session.execute(stmt)
        if flush:
            await session.flush()
        if commit:
            await session.commit()
        return result.rowcount

    async def delete_model_by_pk(
            self,
            session: AsyncSession,
            pk:Any,
            flush:bool= False,
            commit:bool= False,
    )->int:
        """
        根据主键删除数据
        :param session:
        :param pk:
        :param flush:
        :param commit:
        :return:
        """
        stmt=delete(self.model).where(self.primary_key == pk)
        result = await session.execute(stmt)
        if flush:
            await session.flush()
        if commit:
            await session.commit()
        return result.rowcount