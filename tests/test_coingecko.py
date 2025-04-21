# src/tests/test_coingecko.py
import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = str(Path.cwd())
sys.path.append(project_root)
print(f"Project root: {project_root}")

from src.collectors.coingecko import CoinGeckoCollector

async def test_collector():
    # Instantiate the collector
    collector = CoinGeckoCollector()

    records = await collector.collectBTC(days=14)
    for record in records[:5]:  # Print first 5 records
        print(record)


# Run the asynchronous test function
if __name__ == "__main__":
    asyncio.run(test_collector())