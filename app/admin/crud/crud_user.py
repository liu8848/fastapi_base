
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.model.sys_user import User
from app.admin.schema.user import RegisterUserParam
from common.crud.CRUDBase import CRUDBase


class CRUDUser(CRUDBase[User]):
    """
    user表CRUD类
    """

    async def create(self, db: AsyncSession, obj: RegisterUserParam) -> None:
        """
        创建用户
        @param db:
        @param obj:
        @return:
        """

        dict_obj = obj.model_dump()

        new_user = self.model(**dict_obj)
        db.add(new_user)


user_dao: CRUDUser = CRUDUser(User)