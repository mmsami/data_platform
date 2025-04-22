# src/collectors/coingecko.py
from .base import BaseCollector, DataRecord
import aiohttp
from datetime import datetime, timezone
from typing import List

class CoinGeckoCollector(BaseCollector):
    def __init__(self) -> None:
        super().__init__(name="coingecko")
        self.base_url = "https://api.coingecko.com/api/v3"
    
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
                data = await response.json()

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
