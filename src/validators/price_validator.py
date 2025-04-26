# src/validators/price_validator.py
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime, timedelta
import numpy as np

@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str]
    warnings: List[str]

@dataclass
class ValidationThresholds:
    min_price: float = 0
    max_price: float = 1_000_000  # $1M
    max_price_change: float = 0.20  # 20%
    min_data_points: int = 10
    max_time_gap: timedelta = timedelta(hours=1)

class PriceValidator:
    def __init__(self, thresholds: Optional[ValidationThresholds] = None):
        self.thresholds = thresholds or ValidationThresholds()
        self.min_price = self.thresholds.min_price
        self.max_price = self.thresholds.max_price
        self.max_price_change = self.thresholds.max_price_change
    
    def validate_price_data(self, prices: List[float], timestamps: List[datetime]) -> ValidationResult:
        errors = []
        warnings = []

        # Check for negative prices
        if any(p <= self.min_price for p in prices):
            errors.append("Negative or zero prices found")
        
        if len(prices) < self.thresholds.min_data_points:
            errors.append(f"Insufficient data points: {len(prices)}")
        
        for i in range(1, len(timestamps)):
            time_diff = timestamps[i] - timestamps[i-1]
            if time_diff > self.thresholds.max_time_gap:
                warnings.append(f"Large time gap detected: {time_diff} at {timestamps[i]}")

        # Check for sudden price changes
        for i in range(1, len(prices)):
            change = abs(prices[i] - prices[i-1]) / prices[i-1]
            if change > self.max_price_change:
                warnings.append(f"Large price change detected: {change*100:.2f}% at {timestamps[i]}")
        
        if any(p > self.thresholds.max_price for p in prices):
            errors.append(f"Price above maximum threshold ({self.thresholds.max_price})")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )