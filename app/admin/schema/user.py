from datetime import datetime

from common.schema import SchemaBase


class AuthSchemaBase(SchemaBase):
    username: str


class RegisterUserParam(AuthSchemaBase):
    pass

class UserInfoSchemaBase(SchemaBase):
    id:str
    username: str
    create_name:str
    create_time:datetime
    update_time:datetime
    update_user:str