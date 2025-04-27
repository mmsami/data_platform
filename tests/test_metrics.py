# tests/test_metrics.py
import pytest
from src.utils.metrics import MetricsCollector
from datetime import datetime

def test_metrics():
    metrics = MetricsCollector()

    # Test collection start
    metrics.start_collection()
    assert metrics.current_run is not None
    
    
    # Test collection end
    metrics.end_collection(records=10, retries=2, errors=1)
    assert metrics.current_run.records_collected == 10
    assert metrics.current_run.retries == 2
    assert metrics.current_run.end_time > metrics.current_run.start_time
