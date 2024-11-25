
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


    async def get(self, db: AsyncSession, user_id: str) -> User | None:
        """
        获取用户

        :param db:
        :param user_id:
        :return:
        """
        return await self.select_model(db, user_id)


user_dao: CRUDUser = CRUDUser(User)