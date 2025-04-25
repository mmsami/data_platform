# src/analysis/price_analyzer.py
from typing import List, Dict, Tuple
from datetime import datetime
import pandas as pd

class PriceAnalyzer:
    def __init__(self, db_session) -> None:
        self.session = db_session
    
    def get_price_history(self, currency: str, days: int = 30) -> pd.DataFrame:
        """Get price history for analysis"""
        query = f"""
        SELECT price, price_timestamp, currency
        FROM btc_prices
        WHERE currency = %s
        AND price_timestamp >= NOW() - INTERVAL '{days} DAY'
        ORDER BY price_timestamp
        """
        params = (currency,)  # Use a tuple for positional parameters
        return pd.read_sql(query, self.session.bind, params=params)
    
    def calculate_daily_stats(self, currency: str) -> Dict:
        df = self.get_price_history(currency)
        return {
            'mean': df['price'].mean(),
            'std': df['price'].std(),
            'min': df['price'].min(),
            'max': df['price'].max(),
            'last_price': df['price'].iloc[-1]
        }
    
    def compare_currencies(self, currency1: str, currency2: str) -> Dict:
        """Compare prices between currencies"""
        df1 = self.get_price_history(currency1)
        df2 = self.get_price_history(currency2)

        # Calculate correlation and other metrics
        return {
            'correlation': df1['price'].corr(df2['price']),
            'ratio_mean': (df1['price'] / df2['price']).mean()
        }