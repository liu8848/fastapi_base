from fastapi import APIRouter
router = APIRouter()

@router.get("/hello")
async def hello():
    return {"message": "hello world"}

@router.post("/hello/{name}")
async def hello(name: str):
    return {"message": f"hello {name}"}