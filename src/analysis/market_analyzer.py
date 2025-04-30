# src/services/market_analyzer.py

from datetime import datetime, timedelta
from typing import List, Dict
from src.storage.models import BitcoinNews, BTCPrice
from src.storage.analytics import PriceNewsAnalysis
from sqlalchemy import func, and_
from src.utils.logger import logger

class MarketAnalyzer:
    def __init__(self, db):
        self.session = db
    
    def get_price_with_news(self, days: int = 1, currency: str = 'eur') -> List[PriceNewsAnalysis]:
        """Get prices and corresponding news for the specified timeframe"""
        try:
            # Get start date
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)

            # Get prices
            prices = self.session.query(BTCPrice).filter(
                and_(
                    BTCPrice.price_timestamp >= start_date,
                    BTCPrice.price_timestamp <= end_date,
                    BTCPrice.currency == currency
                )
            ).order_by(BTCPrice.price_timestamp).all()

            # Get news
            news = self.session.query(BitcoinNews).filter(
                and_(
                    BitcoinNews.published_at >= start_date,
                    BitcoinNews.published_at <= end_date,
                )
            ).order_by(BitcoinNews.published_at).all()

            # Group news by date
            news_by_date = {}
            for news_item in news:
                date_key = news_item.published_at.date()
                if date_key not in news_by_date:
                    news_by_date[date_key] = []
                news_by_date[date_key].append(news_item)
            
            # Calculate daily analysis
            analysis_results = []
            for i in range(1, len(prices)):
                current_price = prices[i]
                prev_price = prices[i-1]

                # Calculate price change
                price_change = current_price.price - prev_price.price
                price_change_percentage = (price_change / prev_price.price) * 100

                # Get news for this date
                date_key = current_price.price_timestamp.date()
                relevant_news = news_by_date.get(date_key, [])

                analysis = PriceNewsAnalysis(
                    date=current_price.price_timestamp,
                    price_data=current_price,
                    news_items=relevant_news,
                    price_change=price_change,
                    price_change_percentage=price_change_percentage
                )
                analysis_results.append(analysis)
            return analysis_results

        except Exception as e:
            logger.error(f"Error in market analysis: {e}")
            raise
    
    def get_daily_summary(self, currency: str = 'eur') -> Dict:
        """Get today's market summary"""
        try:
            today = datetime.now().date()

            # Get today's price range
            price_data = self.session.query(
                func.min(BTCPrice.price).label('low'),
                func.max(BTCPrice.price).label('high'),
                func.avg(BTCPrice.price).label('average')
            ).filter(
                and_(
                    func.date(BTCPrice.price_timestamp) == today,
                    BTCPrice.currency == currency
                )
            ).first()

            # Get today's news
            news_items = self.session.query(BitcoinNews).filter(
                func.date(BitcoinNews.published_at) == today
            ).all()

            return {
                'date': today,
                'price_summary': {
                    'low': price_data.low if price_data else None,
                    'high': price_data.high if price_data else None,
                    'average': price_data.average if price_data else None
                },
                'news_count': len(news_items),
                'latest_news': [
                    {'title': news.title, 'published_at': news.published_at}
                    for news in news_items[:5]  # Last 5 news items
                ]
            }
        except Exception as e:
            logger.error(f"Error getting daily summary: {e}")
            raise