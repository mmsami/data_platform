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
            price_data = {
                f"price_{record.data['currency']}": record.data["price"]
            }
            processed.append(
                BTCPrice(
                    price=record.data['price'],
                    currency=record.data['currency'],
                    price_timestamp=record.data['timestamp'],
                    collected_at=record.timestamp
                )
            )
        
        return processed