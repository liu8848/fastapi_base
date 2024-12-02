from fastapi import APIRouter

from app.admin.api.user_controller import router as user_router
from app.crawl4ai.api.crawl_controller import router as crawl_router
from core.conf import settings

router = APIRouter(prefix=settings.FASTAPI_API_V1_PATH)

router.include_router(user_router)
router.include_router(crawl_router)