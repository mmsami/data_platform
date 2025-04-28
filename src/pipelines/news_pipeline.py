# src/pipelines/news_pipeline.py

from typing import List
from src.scrapers.bitcoin_news import BitcoinNewsScrapper
from src.storage.models import BitcoinNews
from src.storage.database import DatabaseManager
from src.utils.logger import logger
from datetime import datetime
from sqlalchemy.dialects.postgresql import insert as pg_insert

class BitcoinNewsPipeline:
    def __init__(self):
        self.scraper = BitcoinNewsScrapper()
        self.db = DatabaseManager()
    
    async def run(self) -> List[BitcoinNews]:
        try:
            # Initialize database
            self.db.init_db()
            
            # Scrape news
            news_items = await self.scraper.scrape()
            logger.info(f"Scraped {len(news_items)} news items")

            # Convert to database models
            db_items = []
            for item in news_items:
                db_items.append({
                    'title': item['title'],
                    'summary': item['summary'],
                    'link': item['link'],
                    'published_at': item['published_at'],
                    'source': item['source'],
                    'collected_at': datetime.now()
                })

            # Store in database
            with self.db.get_session() as session:
                # Use upsert to avoid duplicates
                stmt = pg_insert(BitcoinNews.__table__).values(
                    db_items
                ).on_conflict_do_nothing(
                    index_elements=['title', 'published_at']
                )

                result = session.execute(stmt)
                session.commit()
                logger.info(f"Stored {result.rowcount} new articles")
            return db_items
        except Exception as e:
            logger.error(f"News pipeline error: {e}")
            raise