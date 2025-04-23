# src/utils/metrics.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class CollectionMetrics:
    start_time: datetime
    end_time: Optional[datetime] = None
    records_collected: int = 0
    retries: int = 0
    errors: int = 0

class MetricsCollector:
    def __init__(self) -> None:
        self.current_run: Optional[CollectionMetrics] = None
    
    def start_collection(self):
        self.current_run = CollectionMetrics(datetime.now())

    def end_collection(self, records: int = 0, retries: int = 0, errors: int = 0):
        if self.current_run:
            self.current_run.end_time = datetime.now()
            self.current_run.records_collected = records
            self.current_run.retries = retries
            self.current_run.errors = errors

