from typing import Annotated

from fastapi import APIRouter,Path

from app.admin.schema.user import RegisterUserParam
from app.admin.service.user_service import user_service
from common.response.response_schema import ResponseModel, response_base
from utils.serializer import select_as_dict
from app.admin.schema.user import UserInfoSchemaBase

router = APIRouter(prefix="/user", tags=["user"])


@router.post('/register', summary='注册用户')
async def register_user(obj: RegisterUserParam) -> ResponseModel:
    await user_service.register(obj=obj)
    return response_base.success()

@router.get('/get_userinfo/{id}',summary='获取用户信息')
async def get_userinfo(id:Annotated[str,Path(...)]) -> ResponseModel:
    user=await user_service.get_userinfo(id)
    data=UserInfoSchemaBase(**select_as_dict(user))
    return response_base.success(data=data)