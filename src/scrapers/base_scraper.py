# src/scrapers/base_scraper.py

import aiohttp
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from datetime import datetime
from src.utils.rate_limiter import RateLimiter

class BaseScraper(ABC):
    def __init__(self, name: str) -> None:
        self.name = name
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.rate_limiter = RateLimiter(calls_per_minute=10)
    
    async def fetch_page(self, url: str) -> str:
        await self.rate_limiter.wait_if_needed()
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url) as response:
                return await response.text()
    
    @abstractmethod
    async def scrape(self) -> List[Dict[str, Any]]:
        """Must be implemented by each scraper"""
        pass