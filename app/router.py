from fastapi import APIRouter
from core.conf import settings

from app.test.router import router as test_router

router = APIRouter(prefix=settings.FASTAPI_API_V1_PATH)

router.include_router(test_router)
