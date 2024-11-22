from fastapi import APIRouter

from core.conf import settings

router = APIRouter(prefix=settings.FASTAPI_API_V1_PATH)


