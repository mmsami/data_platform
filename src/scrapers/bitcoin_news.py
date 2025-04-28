# src/scrapers/bitcoin_news.py

from typing import Dict, List, Any
from .base_scraper import BaseScraper
import feedparser
from datetime import datetime
from bs4 import BeautifulSoup
import re

class BitcoinNewsScrapper(BaseScraper):
    def __init__(self):
        super().__init__(name="bitcoin_news")
        self.rss_url = "https://www.coindesk.com/arc/outboundfeeds/rss/"

    async def scrape(self) -> List[Dict[str, Any]]:
        feed_content = await self.fetch_page(self.rss_url)
        feed = feedparser.parse(feed_content)

        news_items = []
        for entry in feed.entries:
            # Clean HTML from description
            soup = BeautifulSoup(entry.description, 'html.parser')
            clean_description = soup.get_text()

            news_items.append(
                {
                    'title': entry.title,
                    'summary': clean_description[:500],  # First 500 chars
                    'link': entry.link,
                    'published_at': datetime(*entry.published_parsed[:6]),
                    'source': 'coindesk'
                }
            )
        return news_items