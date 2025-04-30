# tests/test_market_analyzer.py

import pytest
from datetime import datetime, timedelta
from src.analysis.market_analyzer import MarketAnalyzer
from src.storage.models import BTCPrice, BitcoinNews
from src.pipelines.news_pipeline import BitcoinNewsPipeline

@pytest.mark.asyncio
async def test_market_analyzer():
    # Get database session
    pipeline = BitcoinNewsPipeline()

    with pipeline.db.get_session() as session:
        analyzer = MarketAnalyzer(session)
        # Test price with news analysis
        analysis = analyzer.get_price_with_news(days=1)
        assert len(analysis) > 0, "No analysis results"

        # Test first analysis result
        first_analysis = analysis[0]
        assert isinstance(first_analysis.price_change, float)
        assert isinstance(first_analysis.price_change_percentage, float)

        # Test daily summary
        summary = analyzer.get_daily_summary()
        assert 'price_summary' in summary
        assert 'news_count' in summary
        assert 'latest_news' in summary

@pytest.mark.asyncio
async def test_market_analyzer_empty_data():
    pipeline = BitcoinNewsPipeline()
    with pipeline.db.get_session() as session:
        analyzer = MarketAnalyzer(session)
        # Test with future date (should have no data)
        future_analysis = analyzer.get_price_with_news(
            days=1, 
            start_date=datetime.now() + timedelta(days=30)
        )
        assert len(future_analysis) == 0, "Should not have future data"