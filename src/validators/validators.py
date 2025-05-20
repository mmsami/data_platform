# src/quality/validators.py
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import pandas as pd
from src.utils.logger import logger

@dataclass
class QualityCheck:
    name: str
    passed: bool
    message: str
    details: Optional[Dict] = None

@dataclass
class QualityReport:
    timestamp: datetime
    source: str
    checks: List[QualityCheck]
    data_sample: Optional[Dict] = None

    @property
    def passed(self) -> bool:
        return all(check.passed for check in self.checks)
    
    @property
    def summary(self) -> str:
        total = len(self.checks)
        passed = sum(1 for check in self.checks if check.passed)
        return f"Passed {passed}/{total} checks"

class DataQualityValidator:
    def __init__(self):
        self.price_thresholds = {
            'min_price': 1000,  # Minimum reasonable BTC price
            'max_price': 500000,  # Maximum reasonable BTC price
            'max_price_change': 0.20,  # 20% max change between points
            'min_data_points': 10,  # Minimum points expected
            'max_time_gap': timedelta(minutes=10)  # Maximum gap between points
        }
    
    def validate_price_data(self, prices: List[float], timestamps: List[datetime]) -> QualityReport:
        # First, check if we have data to validate
        if not prices or not timestamps:
            return QualityReport(
                timestamp=datetime.now(),
                source="price_data",
                checks=[QualityCheck(
                    name="data_existence",
                    passed=False,
                    message="No data provided for validation",
                    details=None
                )],
                data_sample=None
            )

        try:
            checks = []

            # Check data volume
            volume_check = QualityCheck(
                name="data_volume",
                passed=len(prices) >= self.price_thresholds['min_data_points'],
                message=f"Expected at least {self.price_thresholds['min_data_points']} points, got {len(prices)}"
            )
            checks.append(volume_check)

            # Check price range
            price_range_check = QualityCheck(
                name="price_range",
                passed=all(self.price_thresholds['min_price'] <= p <= self.price_thresholds['max_price'] 
                          for p in prices),
                message=f"Prices should be between {self.price_thresholds['min_price']} and {self.price_thresholds['max_price']}"
            )
            checks.append(price_range_check)

            # Check for sudden changes
            for i in range(1, len(prices)):
                change = abs(prices[i] - prices[i-1]) / prices[i-1]
                if change > self.price_thresholds['max_price_change']:
                    checks.append(QualityCheck(
                        name="price_change",
                        passed=False,
                        message=f"Suspicious price change of {change*100:.1f}% at {timestamps[i]}",
                        details={
                            'timestamp': timestamps[i],
                            'previous_price': prices[i-1],
                            'current_price': prices[i],
                            'change_percentage': change * 100
                        }
                    ))

            # Check time gaps
            for i in range(1, len(timestamps)):
                gap = timestamps[i] - timestamps[i-1]
                if gap > self.price_thresholds['max_time_gap']:
                    checks.append(QualityCheck(
                        name="time_gap",
                        passed=False,
                        message=f"Large time gap of {gap} at {timestamps[i]}",
                        details={
                            'timestamp': timestamps[i],
                            'previous_time': timestamps[i-1],
                            'gap': str(gap)
                        }
                    ))

            # Always return a QualityReport
            return QualityReport(
                timestamp=datetime.now(),
                source="price_data",
                checks=checks,
                data_sample={
                    'first_timestamp': timestamps[0] if timestamps else None,
                    'last_timestamp': timestamps[-1] if timestamps else None,
                    'price_range': [min(prices), max(prices)] if prices else None
                }
            )

        except Exception as e:
            logger.error(f"Error in price validation: {e}")
            return QualityReport(
                timestamp=datetime.now(),
                source="price_data",
                checks=[QualityCheck(
                    name="validation_error",
                    passed=False,
                    message=f"Error during validation: {str(e)}",
                    details=None
                )],
                data_sample=None
            )
    
    def validate_news_data(self, news_items: List[Dict]) -> QualityReport:
        checks = []
        
        # Check volume
        volume_check = QualityCheck(
            name="news_volume",
            passed=len(news_items) > 0,
            message=f"Found {len(news_items)} news items"
        )
        checks.append(volume_check)

        # Check content
        for item in news_items:
            # Title check
            if not item.get('title') or len(item['title']) < 10:
                checks.append(QualityCheck(
                    name="title_quality",
                    passed=False,
                    message=f"Invalid title: {item.get('title')}",
                    details={'item': item}
                ))

            # Summary check
            if not item.get('summary') or len(item['summary']) < 50:
                checks.append(QualityCheck(
                    name="summary_quality",
                    passed=False,
                    message=f"Summary too short for: {item.get('title')}",
                    details={'item': item}
                ))

        return QualityReport(
            timestamp=datetime.now(),
            source="news_data",
            checks=checks,
            data_sample={'sample_size': len(news_items)}
        )

