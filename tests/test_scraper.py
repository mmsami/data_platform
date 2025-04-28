# tests/test_scraper.py
import pytest
from src.scrapers.bitcoin_news import BitcoinNewsScrapper
from datetime import datetime

@pytest.mark.asyncio
async def test_bitcoin_news_scraper():
    # Initialize scraper
    scraper = BitcoinNewsScrapper()

    # Get news items
    news_items = await scraper.scrape()
    # Check first item structure
    first_item = news_items[0]

    # Basic validation
    assert len(news_items) > 0, "No news items scraped"

    # Validate content
    assert len(first_item['title']) > 0, "Empty title"
    assert len(first_item['summary']) > 0, "Empty summary"
    assert first_item['link'].startswith('http'), "Invalid link format"
    assert first_item['source'] == 'coindesk', "Wrong source"

@pytest.mark.asyncio
async def test_scraper_rate_limiting():
    scraper = BitcoinNewsScrapper()
    
    # Test multiple scrapes
    for _ in range(3):
        news_items = await scraper.scrape()
        assert len(news_items) > 0, "Scraping failed after rate limiting"