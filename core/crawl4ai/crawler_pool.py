import asyncio,os
import time

from typing import Dict

from crawl4ai import AsyncWebCrawler

class CrawlerPool:
    def __init__(self,max_size:int=10):
        self.max_size = max_size
        self.active_crawlers:Dict[AsyncWebCrawler,float]={}
        self._lock=asyncio.Lock()

    async def acquire(self,**kwargs)->AsyncWebCrawler:
        async with self._lock:
            # 清理不在运行状态的 crawlers
            current_time=time.time()
            inactive=[
                crawler
                for crawler,last_used in self.active_crawlers.items()
                if current_time-last_used>600 # 超时时间设置为10分钟
            ]
            for crawler in inactive:
                await crawler.__aexit__(None, None, None)
                del self.active_crawlers[crawler]

            # 必要时，创建新的crawler
            if len(self.active_crawlers)<self.max_size:
                crawler=AsyncWebCrawler(**kwargs)
                self.active_crawlers[crawler]=current_time
                return crawler

            # 复用最近用过的crawler
            crawler = min(self.active_crawlers.items(), key=lambda x: x[1])[0]
            self.active_crawlers[crawler]=current_time
            return crawler

    async def release(self,crawler:AsyncWebCrawler):
        async with self._lock:
            if crawler in self.active_crawlers:
                self.active_crawlers[crawler]=time.time()

    async def cleanup(self):
        async with self._lock:
            for crawler in list(self.active_crawlers.keys()):
                await crawler.__aexit__(None, None, None)
            self.active_crawlers.clear()