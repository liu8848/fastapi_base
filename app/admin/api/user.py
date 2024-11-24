
from fastapi import APIRouter

from app.admin.schema.user import RegisterUserParam
from app.admin.service.user_service import user_service
from common.response.response_schema import ResponseModel, response_base

router = APIRouter(prefix="/user", tags=["user"])


@router.post('/register', summary='注册用户')
async def register_user(obj: RegisterUserParam) -> ResponseModel:
    await user_service.register(obj=obj)
    return response_base.success()