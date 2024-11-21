
from common.model import Base,str_id_key

from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String



class User(Base):
    __tablename__ = 'sys_user'

    id: Mapped[str_id_key]=mapped_column(init=False)
    username:Mapped[str]=mapped_column(String(20),index=True,comment='用户名')