# src/pipelines/btc_pipeline.py
from typing import List
from src.collectors.btc_collector import CoinGeckoCollector
from src.processors.btc_processor import BTCProcessor
from src.storage.models import BTCPrice
from src.storage.database import DatabaseManager
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import insert as pg_insert
from src.utils.metrics import MetricsCollector
from src.utils.logger import logger
from src.validators.price_validator import PriceValidator
from src.analysis.price_analyzer import PriceAnalyzer
from src.config.settings import settings

class BTCPipeline:
    def __init__(self):
        self.collector = CoinGeckoCollector()
        self.processor = BTCProcessor()
        self.db = DatabaseManager()
        self.metrics = MetricsCollector()
        self.validator =PriceValidator()

    async def run(self, days : int = 14) -> List[BTCPrice]:
        self.metrics.start_collection()
        try:
            # Initialize database
            self.db.init_db()

            # Collect data
            raw_records = await self.collector.collect(days=days)

            # Process data
            processed_data = self.processor.process_records(raw_records)

            # Validate data before storage
            for currency in settings.SUPPORTED_CURRENCIES:
                currency_data = [r for r in processed_data if r.currency == currency]
                prices = [r.price for r in currency_data]
                timestamps = [r.price_timestamp for r in currency_data]

                validation_result = self.validator.validate_price_data(prices, timestamps)

                if not validation_result.is_valid:
                    logger.error(f"Validation errors for {currency}: {validation_result.errors}")
                if validation_result.warnings:
                    logger.warning(f"Validation warnings for {currency}: {validation_result.warnings}")

            # Store data
            with self.db.get_session() as session:
                # Create insert statement with ON CONFLICT DO NOTHING
                stmt = pg_insert(BTCPrice.__table__).values(
                    [
                        {
                            'price': record.price,
                            'currency': record.currency,
                            'price_timestamp': record.price_timestamp,
                            'collected_at': record.collected_at
                        }
                        for record in processed_data
                    ]
                ).on_conflict_do_nothing(
                    index_elements=['price_timestamp', 'currency']
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

            # Record metrics
            self.metrics.end_collection(
                records=len(processed_data),
                retries=self.collector.retries if hasattr(self.collector, 'retries') else 0
            )

            if self.metrics.current_run:
                duration = (self.metrics.current_run.end_time - self.metrics.current_run.start_time).total_seconds()
                logger.info(f"""
                    Collection Metrics:
                    ------------------
                    Records collected: {self.metrics.current_run.records_collected}
                    Retries: {self.metrics.current_run.retries}
                    Duration: {duration:.2f} seconds
                    Start time: {self.metrics.current_run.start_time}
                    End time: {self.metrics.current_run.end_time}
                                    """)
     
            return processed_data
        except Exception as e:
            self.metrics.end_collection(errors=1)
            logger.error(f"Pipeline error: {e}")
            raise


