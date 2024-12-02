
from app.admin.model.sys_user import User
from common.crud.base_mapper import BaseMapper


class UserMapper(BaseMapper[User]):
    """
    user表CRUD类
    """
    pass


user_dao: UserMapper = UserMapper(User)