from app.admin.crud.crud_user import user_dao
from app.admin.schema.user import RegisterUserParam
from database.db_mysql import async_db_session

from common.crud.base_service import BaseService
from app.admin.model.sys_user import User

class UserService(BaseService[User]):

    @staticmethod
    async def register(*, obj: RegisterUserParam) -> None:
        async with async_db_session.begin() as db:
            await user_dao.create_model(db, obj)


user_service: UserService = UserService(User)