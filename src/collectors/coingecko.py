# src/collectors/coingecko.py
from .base import BaseCollector, DataRecord
import aiohttp
import asyncio
from datetime import datetime, timezone
from typing import List
from ..config.settings import settings
from src.utils.rate_limiter import RateLimiter

class CoinGeckoCollector(BaseCollector):
    def __init__(self) -> None:
        super().__init__(name="coingecko")
        self.base_url = settings.COINGECKO_BASE_URL
        self.rate_limiter = RateLimiter(calls_per_minute=settings.RATE_LIMIT_CALLS)
        self.max_retries = 3
        self.retries = 0
    
    async def _make_request(self, url: str, params: dict = None) -> dict:
        """Make API request with retry logic"""
        for attempt in range(self.max_retries):
            try:
                # Wait for rate limit
                await self.rate_limiter.wait_if_needed()

                async with aiohttp.ClientSession() as session:
                    async with session.get(url, params=params) as response:
                        if response.status == 429: # Rate limit hit
                            wait_time = int(response.headers.get('Retry-After', 60))
                            await asyncio.sleep(wait_time)
                            continue
                        response.raise_for_status()
                        return await response.json()
            except aiohttp.ClientError as e:
                self.retries += 1
                if attempt == self.max_retries -1:
                    raise
                await asyncio.sleep(2 ** attempt) # Exponential backoff
        
        raise Exception("Max retries reached")

    
    async def collectBTC(self, days: int = 14) -> List[DataRecord]:
        """
        Fetch historical price data for Bitcoin over the specified number of days.
        """
        url = f"{self.base_url}/coins/bitcoin/market_chart"
        params = {
            "vs_currency": "eur",  # Target currency: EUR
            "days": days           # Number of days to fetch historical data
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                data = await self._make_request(url, params)

                # Extract prices from the response
                prices = data.get("prices", [])

                return [
                    DataRecord(
                        source=self.name,
                        data={"timestamp": datetime.fromtimestamp(price[0] / 1000, timezone.utc), "price": price[1]},
                        timestamp=datetime.now(timezone.utc).isoformat()
                    )
                    for price in prices
                ]

    async def collect(self, days: int = 14) -> List[DataRecord]:
        """
        Implementation of the base collector interface.
        By default, collects BTC data for the last 14 days.
        """
        return await self.collectBTC(days=days)
