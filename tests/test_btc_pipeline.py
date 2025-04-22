# src/tests/test_btc_pipeline.py
import asyncio
import pytest
import os
from src.pipelines.btc_pipeline import BTCPipeline

@pytest.mark.asyncio
async def test_btc_pipeline():
    # Debug: Print the database URL (masking password)
    db_url = os.getenv('DATABASE_URL')
    # if db_url:
    #     # Mask the password in the URL for security
    #     masked_url = db_url.split('@')[0] + '@' + db_url.split('@')[1] if '@' in db_url else db_url
    #     print(f"\nDatabase URL: {masked_url}")
    # else:
    #     print("\nNo DATABASE_URL found in environment")
    
    # Verify database connection is configured
    assert db_url, "DATABASE_URL not found in environment"
    
    pipeline = BTCPipeline()
    records = await pipeline.run(days=1)  # Reduced to 1 day for testing
    
    # Verify we got records
    assert len(records) > 0, "No records were processed"
    
    # Verify record structure
    first_record = records[0]
    assert hasattr(first_record, 'price_eur'), "Record missing price_eur"
    assert hasattr(first_record, 'price_timestamp'), "Record missing price_timestamp"
    assert hasattr(first_record, 'collected_at'), "Record missing collected_at"
    
    # Print some debug info
    print(f"\nSuccessfully processed {len(records)} records")
    print("\nFirst 5 records:")
    for record in records[:5]:
        print(f"{record}")

if __name__ == "__main__":
    asyncio.run(test_btc_pipeline())
    
