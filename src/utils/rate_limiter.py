# src/utils/rate_limiter.py
import time
import asyncio
from datetime import datetime, timedelta
from collections import deque

class RateLimiter:
    def __init__(self, calls_per_minute: int = 50) -> None:
        self.calls_per_minute = calls_per_minute
        self.calls = deque(maxlen=calls_per_minute)
    
    async def wait_if_needed(self):
        now = datetime.now()

        # Remove old timestamps
        while self.calls and self.calls[0] < now - timedelta(minutes=1):
            self.calls.popleft()
        
        # If we've hit the limit, wait
        if len(self.calls) >= self.calls_per_minute:
            wait_time = (self.calls[0] + timedelta(minutes=1) - now).total_seconds()
            if wait_time > 0:
                await asyncio.sleep(wait_time)
        
        self.calls.append(now)

