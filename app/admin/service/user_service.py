from app.admin.crud.crud_user import user_dao
from app.admin.model import User
from app.admin.schema.user import RegisterUserParam
from common.exception import errors
from database.db_mysql import async_db_session


class UserService:

    @staticmethod
    async def register(*, obj: RegisterUserParam) -> None:
        async with async_db_session.begin() as db:
            await user_dao.create_model(db, obj)

    @staticmethod
    async def get_userinfo(*,id:str)->User:
        async with async_db_session.begin() as db:
            user=await user_dao.select_model(db,id)
            if not user:
                raise  errors.NotFoundError(msg='用户不存在')
            return user

user_service: UserService = UserService()