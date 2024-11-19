from fastapi import APIRouter
from app.test.hello.hello import router as hello_router

router = APIRouter()

router.include_router(hello_router)