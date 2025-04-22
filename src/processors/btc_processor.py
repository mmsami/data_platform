# src/processors/btc_processor.py
from typing import List
from src.collectors.base import DataRecord
from src.storage.models import BTCPrice

class BTCProcessor:
    def process_records(self, records: List[DataRecord]) -> List[BTCPrice]:
        """Converts DataRecords to BTCPrice database models"""
        processed = []
        for record in records:
            # Here we could add business logic like:
            # - Currency conversion
            # - Data validation
            # - Calculating additional metrics
            # - Filtering unwanted data
            processed.append(
                BTCPrice(
                    price_eur = record.data["price"],
                    price_timestamp = record.data["timestamp"],
                    collected_at=record.timestamp
                )
            )
        
        return processed