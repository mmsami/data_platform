# tests/test_news_pipeline.py

# from src.storage.database import DatabaseManager
import warnings
import pytest
from src.pipelines.news_pipeline import BitcoinNewsPipeline
from src.storage.models import BitcoinNews

@pytest.fixture(autouse=True)
def suppress_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning, module="feedparser.html")

@pytest.mark.asyncio
async def test_news_pipeline():
    pipeline = BitcoinNewsPipeline()
    
    try:
        # Create tables first
        # Base.metadata.create_all(pipeline.db.engine)

        results = await pipeline.run()
        
        # Test if data was scraped
        assert len(results) > 0, "No news items processed"
        
        # Check database
        with pipeline.db.get_session() as session:
            stored_items = session.query(BitcoinNews).all()
            assert len(stored_items) > 0, "No items stored in database"
            
            # Test first item
            first_item = stored_items[0]
            assert first_item.title is not None, "Title is missing"
            assert first_item.summary is not None, "Summary is missing"
            assert first_item.published_at is not None, "Published date is missing"
            
    except Exception as e:
        pytest.fail(f"Pipeline test failed: {str(e)}")