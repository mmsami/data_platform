# src/collectors/coingecko.py
from .base import BaseCollector, DataRecord
import aiohttp
import asyncio
from datetime import datetime, timezone
from typing import List
from src.config.settings import settings
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
        data_records = []
        for currency in settings.SUPPORTED_CURRENCIES:
            url = f"{self.base_url}/coins/bitcoin/market_chart"
            params = {
                "vs_currency": currency,  
                "days": days           # Number of days to fetch historical data
            }

            data = await self._make_request(url, params)
            # Extract prices from the response
            prices = data.get("prices", [])

            for price in prices:
                data_records.append(
                    DataRecord(
                        source=self.name,
                        data={
                            "price": price[1],
                            "currency": currency,
                            "timestamp": datetime.fromtimestamp(price[0] / 1000, timezone.utc)
                        },
                        timestamp=datetime.now(timezone.utc)
                    )
                )
        return data_records
        
        
    async def collect(self, days: int = 14) -> List[DataRecord]:
        """
        Implementation of the base collector interface.
        By default, collects BTC data for the last 14 days.
        """
        return await self.collectBTC(days=days)

class BinanceCollector(BaseCollector):
    def __init__(self) -> None:
        super().__init__(name="binance")
        self.base_url = settings.BINANCE_BASE_URL
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
                        if response.status == 429:  # Rate limit hit
                            wait_time = int(response.headers.get('Retry-After', 60))
                            await asyncio.sleep(wait_time)
                            continue
                        response.raise_for_status()
                        return await response.json()
            except aiohttp.ClientError as e:
                self.retries += 1
                if attempt == self.max_retries - 1:
                    raise
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
        
        raise Exception("Max retries reached")

    async def collectBTC(self, days: int = 14) -> List[DataRecord]:
        """
        Fetch historical price data for Bitcoin over the specified number of days.
        """
        data_records = []
        for currency in settings.SUPPORTED_CURRENCIES:
            url = f"{self.base_url}/klines"
            params = {
                "symbol": f"BTC{currency.upper()}",
                "interval": "1d",
                "limit": days
            }

            data = await self._make_request(url, params)
            
            for kline in data:
                # Binance kline format: [OpenTime, Open, High, Low, Close, Volume, ...]
                data_records.append(
                    DataRecord(
                        source=self.name,
                        data={
                            "price": float(kline[4]),  # Closing price
                            "currency": currency,
                            "timestamp": datetime.fromtimestamp(kline[0] / 1000, timezone.utc)
                        },
                        timestamp=datetime.now(timezone.utc)
                    )
                )
        return data_records
    
    async def collect(self, days: int = 14) -> List[DataRecord]:
        """
        Implementation of the base collector interface.
        By default, collects BTC data for the last 14 days.
        """
        return await self.collectBTC(days=days)

class KrakenCollector(BaseCollector):
    def __init__(self) -> None:
        super().__init__(name="kraken")
        self.base_url = settings.KRAKEN_BASE_URL
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
                        if response.status == 429:  # Rate limit hit
                            wait_time = int(response.headers.get('Retry-After', 60))
                            await asyncio.sleep(wait_time)
                            continue
                        response.raise_for_status()
                        return await response.json()
            except aiohttp.ClientError as e:
                self.retries += 1
                if attempt == self.max_retries - 1:
                    raise
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
        
        raise Exception("Max retries reached")

    async def collectBTC(self, days: int = 14) -> List[DataRecord]:
        """
        Fetch historical price data for Bitcoin over the specified number of days.
        """
        data_records = []
        for currency in settings.SUPPORTED_CURRENCIES:
            url = f"{self.base_url}/OHLC"
            params = {
                "pair": f"XBT{currency.upper()}",
                "interval": 1440,  # 1 day in minutes
                "since": int((datetime.now(timezone.utc).timestamp() - days * 86400))
            }

            data = await self._make_request(url, params)
            pair = f"XBT{currency.upper()}"
            
            for timestamp, ohlc in data[pair].items():
                data_records.append(
                    DataRecord(
                        source=self.name,
                        data={
                            "price": float(ohlc[4]),  # Closing price
                            "currency": currency,
                            "timestamp": datetime.fromtimestamp(int(timestamp), timezone.utc)
                        },
                        timestamp=datetime.now(timezone.utc)
                    )
                )
        return data_records
    
    async def collect(self, days: int = 14) -> List[DataRecord]:
        """
        Implementation of the base collector interface.
        By default, collects BTC data for the last 14 days.
        """
        return await self.collectBTC(days=days)