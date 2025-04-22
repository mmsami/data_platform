# src/pipelines/btc_pipeline.py
from typing import List
from src.collectors.coingecko import CoinGeckoCollector
from src.processors.btc_processor import BTCProcessor
from src.storage.models import BTCPrice
from src.storage.database import DatabaseManager
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import insert as pg_insert

class BTCPipeline:
    def __init__(self):
        self.collector = CoinGeckoCollector()
        self.processor = BTCProcessor()
        self.db = DatabaseManager()

    async def run(self, days : int = 14) -> List[BTCPrice]:
        try:
            # Initialize database
            self.db.init_db()

            # Collect data
            raw_records = await self.collector.collect(days=days)

            # Process data
            processed_data = self.processor.process_records(raw_records)

            # Store data
            with self.db.get_session() as session:
                # Create insert statement with ON CONFLICT DO NOTHING
                stmt = pg_insert(BTCPrice.__table__).values(
                    [
                        {
                            'price_eur': record.price_eur,
                            'price_timestamp': record.price_timestamp,
                            'collected_at': record.collected_at
                        }
                        for record in processed_data
                    ]
                ).on_conflict_do_nothing(
                    index_elements=['price_timestamp']
                )

                # Execute the statement
                result = session.execute(stmt)
                session.commit()

                # Log results
                total_records = len(processed_data)
                inserted_records = result.rowcount
                skipped_records = total_records - inserted_records

                print(f"Total records processed: {total_records}")
                print(f"New records inserted: {inserted_records}")
                print(f"Duplicate records skipped: {skipped_records}")
     
            return processed_data
        except Exception as e:
            print(f"Pipeline error: {e}")
            raise


