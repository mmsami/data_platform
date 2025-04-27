# tests/test_rate_limiter.py
import pytest
import asyncio
from src.utils.rate_limiter import RateLimiter
from datetime import datetime, timedelta

@pytest.mark.asyncio
async def test_rate_limiter():
    limiter = RateLimiter(calls_per_minute=2)

    # First two calls should be immediate
    start = datetime.now()
    await limiter.wait_if_needed()
    await limiter.wait_if_needed()
    duration = datetime.now() - start
    assert duration.total_seconds() < 1, "First calls took too long"

    # Third call should wait
    await limiter.wait_if_needed()
    duration = datetime.now() - start
    assert duration.total_seconds() >= 60, "Rate limit not enforced"