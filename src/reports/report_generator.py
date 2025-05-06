# src/reports/report_generator.py

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Dict
import pandas as pd
from src.analysis.market_analyzer import MarketAnalyzer
from src.alerts.alert_manager import AlertManager
from src.utils.logger import logger

@dataclass
class MarketReport:
    date: datetime
    price_summary: Dict
    significant_moves: List[Dict]
    news_summary: Dict
    alerts: List[str]

class ReportGenerator:
    def __init__(self, analyzer: MarketAnalyzer) -> None:
        self.analyzer = analyzer
        self.alert_manager = AlertManager()

    def generate_daily_report(self) -> MarketReport:
        try:
            # Get daily summary
            daily_summary = self.analyzer.get_daily_summary()

            # Get price changes with news
            analysis = self.analyzer.get_price_with_news(days=1)

            # Find significant moves
            significant_moves = [
                {
                    'timestamp': item.date,
                    'price_change': item.price_change_percentage,
                    'news': [news.title for news in item.news_items]
                }
                for item in analysis
                if abs(item.price_change_percentage) > 2.0  # 2% threshold
            ]

            # Generate alerts
            alerts = []
            for move in significant_moves:
                price_alerts = self.alert_manager.check_price_alerts(
                    move['price_change']
                )
                alerts.extend(price_alerts)
            return MarketReport(
                date=datetime.now(),
                price_summary=daily_summary['price_summary'],
                significant_moves=significant_moves,
                 news_summary={
                    'count': daily_summary['news_count'],
                    'latest': daily_summary['latest_news']
                },
                alerts=alerts
            )
        except Exception as e:
            logger.error(f"Error generating daily report: {e}")
            raise
    
    def generate_weekly_report(self) -> MarketReport:
        try:
            # Get weekly data
            analysis = self.analyzer.get_price_with_news(days=7)
            
            # Calculate weekly stats
            prices = []
            for item in analysis:
                prices.append(item.price_data.price)
                
            weekly_summary = {
                'start_price': prices[0],
                'end_price': prices[-1],
                'high': max(prices),
                'low': min(prices),
                'change_percentage': ((prices[-1] - prices[0]) / prices[0]) * 100
            }
            
            # Generate alerts from price changes
            alerts = self.alert_manager.check_price_alerts(
                weekly_summary['change_percentage']
            )
            
            # Get significant moves
            significant_moves = []
            for item in analysis:
                if abs(item.price_change_percentage) > 5.0:
                    significant_moves.append({
                        'timestamp': item.date,
                        'price_change': item.price_change_percentage,
                        'news': [news.title for news in item.news_items]
                    })
            
            # Collect all news
            all_news = []
            for item in analysis:
                all_news.extend(item.news_items)
            
            return MarketReport(
                date=datetime.now(),
                price_summary=weekly_summary,
                significant_moves=significant_moves,
                news_summary={
                    'count': len(all_news),
                    'major_headlines': [news.title for news in all_news[:5]]
                },
                alerts=alerts  # Use price alerts only
            )
            
        except Exception as e:
            logger.error(f"Error generating weekly report: {e}")
            raise