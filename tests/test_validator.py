# tests/test_validator.py
import pytest
from datetime import datetime, timedelta
from src.validators.price_validator import PriceValidator

def test_validator():
    validator = PriceValidator()

    # Test normal case
    timestamps = [datetime.now(), datetime.now() + timedelta(hours=1)]
    prices = [50000, 51000]
    result = validator.validate_price_data(prices=prices, timestamps=timestamps)
    assert result.is_valid, "Valid data marked as invalid"

    # Test price too high
    prices = [1_000_001, 1_000_002]  # Above max threshold
    result = validator.validate_price_data(prices, timestamps)
    assert not result.is_valid, "Invalid high prices not caught"

    # Test negative prices
    prices = [-100, -200]
    result = validator.validate_price_data(prices, timestamps)
    assert not result.is_valid, "Negative prices not caught"