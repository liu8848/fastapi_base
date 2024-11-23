from fastapi import APIRouter

from core.conf import settings
from app.admin.api.user import router as user_router

router = APIRouter(prefix=settings.FASTAPI_API_V1_PATH)

router.include_router(user_router)
