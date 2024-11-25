from datetime import datetime

from common.schema import SchemaBase


class AuthSchemaBase(SchemaBase):
    username: str


class RegisterUserParam(AuthSchemaBase):
    pass

class UserInfoSchemaBase(SchemaBase):
    id:str
    username: str
    create_name:str | None = None
    create_time:datetime | None =None
    update_time:datetime | None =None
    update_user:str | None = None