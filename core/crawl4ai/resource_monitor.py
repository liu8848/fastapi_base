import math
import time

import psutil


class ResourceMonitor:
    def __init__(self,max_concurrent_tasks:int=10):
        self.max_concurrent_tasks = max_concurrent_tasks
        self.memory_threshold=0.85
        self.cpu_threshold=0.90
        self._last_check=0
        self._check_interval=1 # second
        self._last_available_slots=max_concurrent_tasks

    async def get_available_slots(self)->int:
        current_time = time.time()
        if current_time-self._last_check<self._check_interval:
            return self._last_available_slots

        mem_usage=psutil.virtual_memory().percent/100
        cpu_usage=psutil.cpu_percent()/100

        memory_factor=max(0,(self.memory_threshold-mem_usage)/self.memory_threshold)
        cpu_factor=max(0,(self.cpu_threshold-cpu_usage)/self.cpu_threshold)

        self._last_available_slots=math.floor(
            self.max_concurrent_tasks*min(memory_factor,cpu_factor)
        )

        self._last_check=current_time
        return self._last_available_slots

