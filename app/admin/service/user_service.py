from app.admin.crud.crud_user import user_dao
from app.admin.schema.user import RegisterUserParam
from database.db_mysql import async_db_session


class UserService:

    @staticmethod
    async def register(*, obj: RegisterUserParam) -> None:
        async with async_db_session.begin() as db:
            await user_dao.create_model(db, obj)
            # await user_dao.create(db,obj)


user_service: UserService = UserService()