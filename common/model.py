from datetime import datetime
from typing import Annotated

from sqlalchemy import String
from sqlalchemy.orm import Mapped,mapped_column,DeclarativeBase,declared_attr,MappedAsDataclass

from utils.snowflake_generator import generate_unique_id
from utils.timezone import timezone

str_id_key=Annotated[
    str,mapped_column(String(32),primary_key=True,index=True,comment="主键id",default=generate_unique_id)
]

id_key = Annotated[
    int, mapped_column(primary_key=True, index=True, autoincrement=True, sort_order=-999, comment='主键id')
]

class UserMixin(MappedAsDataclass):
    create_user:Mapped[str]=mapped_column(String(20),comment='创建人',default='admin',init=False)
    update_user:Mapped[str]=mapped_column(String(20),comment='修改人',default='admin',init=False)

class DatetimeMixin(MappedAsDataclass):
    create_time:Mapped[datetime]=mapped_column(
        init=False,default_factory=timezone.now,sort_order=999,comment='创建时间'
    )
    update_time:Mapped[datetime]=mapped_column(
        init=False,onupdate=timezone.now(),sort_order=999,comment='更新时间'
    )


class MappedBase(DeclarativeBase):
    """
    声明性基类，封装原始的DeclarativeBase类，作为所有基类或模型类的父类
    """
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

class DataClassBase(MappedAsDataclass,MappedBase):
    """声明性数据基类，带有数据集成"""
    __abstract__ = True


class Base(DataClassBase,DatetimeMixin,UserMixin):
    __abstract__ = True