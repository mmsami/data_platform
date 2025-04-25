# src/validators/price_validator.py
from dataclasses import dataclass
from typing import List
from datetime import datetime
import numpy as np

@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str]
    warnings: List[str]

class PriceValidator:
    def __init__(self) -> None:
        self.max_price_change = 0.20 # 20% max change between prices
        self.min_price = 0
    
    def validate_price_data(self, prices: List[float], timestamps: List[datetime]) -> ValidationResult:
        errors = []
        warnings = []

        # Check for negative prices
        if any(p <= self.min_price for p in prices):
            errors.append("Negative or zero prices found")
        
        # Check for sudden price changes
        for i in range(1, len(prices)):
            change = abs(prices[i] - prices[i-1]) / prices[i-1]
            if change > self.max_price_change:
                warnings.append(f"Large price change detected: {change*100:.2f}% at {timestamps[i]}")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )