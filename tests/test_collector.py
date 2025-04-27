# src/tests/test_coingecko.py
import asyncio
import pytest
from collectors.btc_collector import CoinGeckoCollector

# import sys
# from pathlib import Path

# Add project root to path
# project_root = str(Path.cwd())
# sys.path.append(project_root)
# print(f"Project root: {project_root}")

# from src.collectors.coingecko import CoinGeckoCollector

@pytest.mark.asyncio
async def test_btc_collector():
    # Instantiate the collector
    collector = CoinGeckoCollector()

    records = await collector.collect(days=14)
    assert len(records) > 0  # basic check
    
    # Print directly to sys.stdout to bypass pytest capture
    print("\nFirst 5 records from CoinGecko:")
    for record in records[:5]:
        print(f"{record}")

    # Capture printed output
    # captured = capsys.readouterr()
    # print(captured.out)

    # Check if some expected text is in the output
    # assert "source='coingecko'" in captured.out


# Run the asynchronous test function
if __name__ == "__main__":
    asyncio.run(test_collector())