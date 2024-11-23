


from common.schema import SchemaBase

class AuthSchemaBase(SchemaBase):
    username:str


class RegisterUserParam(AuthSchemaBase):
    pass