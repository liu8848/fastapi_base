from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from common.model import Base, str_id_key


class User(Base):
    __tablename__ = 'sys_user'

    id: Mapped[str_id_key] = mapped_column(init=False)
    username: Mapped[str] = mapped_column(String(20), index=True, comment='用户名')
