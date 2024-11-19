from fastapi import APIRouter
from app.test.hello import router as hello_router

router = APIRouter(prefix="/test", tags=["测试接口"])

router.include_router(hello_router)