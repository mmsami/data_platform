# src/models/analytics.py

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from src.storage.models import BitcoinNews, BTCPrice

@dataclass
class PriceNewsAnalysis:
    date: datetime
    price_data: BTCPrice
    news_items: List[BitcoinNews]
    price_change: float
    price_change_percentage: float