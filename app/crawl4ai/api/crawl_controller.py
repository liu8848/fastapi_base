
from typing import Dict

import psutil
from fastapi import APIRouter,HTTPException, Request

from core.crawl4ai.crawler_model import CrawlRequest, TaskStatus
from core.crawl4ai.crawler_service import crawler_service

router = APIRouter(prefix="/crawl", tags=["crawl"])


@router.get('/health',summary='健康情况')
async def health_check():
    available_slots = await crawler_service.resource_monitor.get_available_slots()
    memory = psutil.virtual_memory()
    return {
        "status": "healthy",
        "available_slots": available_slots,
        "memory_usage": memory.percent,
        "cpu_usage": psutil.cpu_percent(),
    }

@router.post("/crawl")
async def crawl(request: CrawlRequest) -> Dict[str, str]:
    task_id = await crawler_service.submit_task(request)
    return {"task_id": task_id}

@router.get("/task/{task_id}")
async def get_task_status(task_id: str):
    task_info = crawler_service.task_manager.get_task(task_id)
    if not task_info:
        raise HTTPException(status_code=404, detail="Task not found")

    response = {
        "status": task_info.status,
        "created_at": task_info.created_at,
    }

    if task_info.status == TaskStatus.COMPLETED:
        # Convert CrawlResult to dict for JSON response
        if isinstance(task_info.result, list):
            response["results"] = [result.dict() for result in task_info.result]
        else:
            response["result"] = task_info.result.dict()
    elif task_info.status == TaskStatus.FAILED:
        response["error"] = task_info.error

    return response