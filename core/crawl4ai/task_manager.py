import asyncio
from dataclasses import dataclass
import time
from typing import Dict, Optional, Union, List,Any

from core.crawl4ai.crawler_model import CrawlResult,TaskStatus,CrawlRequest

from common.log.loguru_cofig import log



@dataclass
class TaskInfo:
    id:str
    status:TaskStatus
    request: Optional[Union[CrawlRequest, List[CrawlRequest]]] = None
    result:Optional[Union[CrawlResult,List[CrawlResult]]]=None
    error:Optional[str]=None
    created_at:float=time.time()
    ttl:int=3600


class TaskManager:
    def __init__(self,cleanup_interval:int=300):
        self.tasks:Dict[str,TaskInfo]={}
        self.high_priority=asyncio.PriorityQueue()
        self.low_priority=asyncio.PriorityQueue()
        self.cleanup_interval=cleanup_interval
        self.cleanup_task=None

    async def start(self):
        self.cleanup_task=asyncio.create_task(self._cleanup_loop())

    async def stop(self):
        if self.cleanup_task:
            self.cleanup_task.cancel()
            try:
                await self.cleanup_task
            except asyncio.CancelledError:
                pass

    async def add_task(self,task_id:str,priority:int,ttl:int)->None:
        task_info=TaskInfo(id=task_id,status=TaskStatus.PENDING,ttl=ttl)
        self.tasks[task_id]=task_info
        queue=self.high_priority if priority > 5 else self.low_priority
        await queue.put((-priority,task_id))

    async def get_next_task(self)->Optional[str]:
        try:
            _,task_id=await asyncio.wait_for(self.high_priority.get(),timeout=0.1)
            return task_id
        except asyncio.TimeoutError:
            try:
                _,task_id=await asyncio.wait_for(self.low_priority.get(),timeout=0.1)
                return task_id
            except asyncio.TimeoutError:
                return None

    def update_task(
            self,task_id:str,
            status:TaskStatus,
            result:Any=None,
            error:str=None,
    )->None:
        if task_id in self.tasks:
            task_info=self.tasks[task_id]
            task_info.status=status
            task_info.result=result
            task_info.error=error

    def get_task(self,task_id:str)->Optional[TaskInfo]:
        return self.tasks.get(task_id)

    async def _cleanup_loop(self):
        while True:
            try:
                await asyncio.sleep(self.cleanup_interval)
                current_time = time.time()
                expired_tasks=[
                    task_id
                    for task_id,task in self.tasks.items()
                    if current_time-task.created_at>task.ttl
                    and task.status in [TaskStatus.COMPLETED,TaskStatus.FAILED]
                ]
                for task_id in expired_tasks:
                    del self.tasks[task_id]
            except Exception as e:
                log.error(f"Error in cleanup loop: {e}")

