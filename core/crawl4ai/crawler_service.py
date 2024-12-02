import asyncio
import uuid

from crawl4ai.extraction_strategy import (
    LLMExtractionStrategy,
    CosineStrategy,
    JsonCssExtractionStrategy,
)

from core.crawl4ai.crawler_model import TaskStatus, ExtractionConfig, CrawlerType, CrawlRequest
from core.crawl4ai.resource_monitor import ResourceMonitor
from core.crawl4ai.task_manager import TaskManager
from core.crawl4ai.crawler_pool import CrawlerPool

from common.log.loguru_cofig import log

class CrawlerService:
    def __init__(self,max_concurrent_tasks:int=10):
        self.resource_monitor=ResourceMonitor(max_concurrent_tasks)
        self.task_manager=TaskManager()
        self.crawler_pool=CrawlerPool(max_concurrent_tasks)
        self._processing_task=None

    async def start(self):
        log.info("------------运行crawl4ai服务-------------------------")
        await self.task_manager.start()
        self._processing_task = asyncio.create_task(self._process_queue())

    async def stop(self):
        log.info("------------关闭crawl4ai服务-------------------------")
        if self._processing_task:
            self._processing_task.cancel()
            try:
                await self._processing_task
            except asyncio.CancelledError:
                pass
        await self.task_manager.stop()
        await self.crawler_pool.cleanup()

    def _create_extraction_strategy(self, config: ExtractionConfig):
        if not config:
            return None

        if config.type == CrawlerType.LLM:
            return LLMExtractionStrategy(**config.params)
        elif config.type == CrawlerType.COSINE:
            return CosineStrategy(**config.params)
        elif config.type == CrawlerType.JSON_CSS:
            return JsonCssExtractionStrategy(**config.params)
        return None

    async def submit_task(self, request: CrawlRequest) -> str:
        task_id = str(uuid.uuid4())
        await self.task_manager.add_task(task_id, request.priority, request.ttl or 3600)

        # Store request data with task
        self.task_manager.tasks[task_id].request = request

        return task_id

    async def _process_queue(self):
        while True:
            try:
                available_slots=await self.resource_monitor.get_available_slots()
                if False and available_slots<=0:
                    await asyncio.sleep(1)
                    continue

                task_id=await self.task_manager.get_next_task()
                if not task_id:
                    await asyncio.sleep(1)
                    continue

                task_info=self.task_manager.get_task(task_id)
                if not task_info:
                    continue

                request = task_info.request
                self.task_manager.update_task(task_id, TaskStatus.PROCESSING)

                try:
                    crawler=await self.crawler_pool.acquire(**request.crawler_params)

                    extraction_strategy = self._create_extraction_strategy(request.extraction_config)

                    if isinstance(request.urls, list):
                        results = await crawler.arun_many(
                            urls=[str(url) for url in request.urls],
                            extraction_strategy=extraction_strategy,
                            js_code=request.js_code,
                            wait_for=request.wait_for,
                            css_selector=request.css_selector,
                            screenshot=request.screenshot,
                            magic=request.magic,
                            **request.extra,
                        )
                    else:
                        results = await crawler.arun(
                            url=str(request.urls),
                            extraction_strategy=extraction_strategy,
                            js_code=request.js_code,
                            wait_for=request.wait_for,
                            css_selector=request.css_selector,
                            screenshot=request.screenshot,
                            magic=request.magic,
                            **request.extra,
                        )
                    await self.crawler_pool.release(crawler)
                    self.task_manager.update_task(task_id, TaskStatus.COMPLETED, results)
                except Exception as e:
                    log.error(f"Error processing task {task_id}: {str(e)}")
                    self.task_manager.update_task(task_id, TaskStatus.FAILED, error=str(e))
            except Exception as e:
                log.error(f"Error in queue processing: {str(e)}")
                await asyncio.sleep(1)

crawler_service = CrawlerService()