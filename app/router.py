from fastapi import APIRouter

from app.test.router import router as test_router
from core.conf import settings

router = APIRouter(prefix=settings.FASTAPI_API_V1_PATH)

router.include_router(test_router)
