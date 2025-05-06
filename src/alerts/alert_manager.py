# src/alerts/alert_manager.py

from typing import List
from datetime import datetime

class AlertManager:
    def __init__(self):
        self.price_thresholds = {
            'critical': 10.0,  # 10% change
            'high': 5.0,      # 5% change
            'medium': 2.0     # 2% change
        }
    
    def check_price_alerts(self, price_change: float) -> List[str]:
        alerts = []
        abs_change = abs(price_change)
        direction = "increase" if price_change > 0 else "decrease"
        
        if abs_change >= self.price_thresholds['critical']:
            alerts.append(f"CRITICAL ALERT: {abs_change:.1f}% price {direction}")
        elif abs_change >= self.price_thresholds['high']:
            alerts.append(f"HIGH ALERT: {abs_change:.1f}% price {direction}")
        elif abs_change >= self.price_thresholds['medium']:
            alerts.append(f"MEDIUM ALERT: {abs_change:.1f}% price {direction}")
            
        return alerts
    
    def check_news_alerts(self, news_items: List) -> List[str]:
        alerts = []
        keywords = ['hack', 'ban', 'regulation', 'crash', 'surge']

        for news in news_items:
            for keyword in keywords:
                if keyword in news.title.lower():
                    alerts.append(f"NEWS ALERT: Found '{keyword}' in news")
                    
        return alerts