# src/pipelines/btc_pipeline.py
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

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
from src.utils.exceptions import ValidationError, CollectionError
from src.utils.error_tracker import ErrorTracker
from src.validators.validators import DataQualityValidator
from src.storage.quality_storage import QualityCheckResult

class BTCPipeline:
    def __init__(self):
        self.collector = CoinGeckoCollector()
        self.processor = BTCProcessor()
        self.db = DatabaseManager()
        self.metrics = MetricsCollector()
        self.validator = PriceValidator()
        self.error_tracker = ErrorTracker()
        self.quality_validator = DataQualityValidator()

    async def run(self, days : int = 14) -> List[BTCPrice]:
        self.metrics.start_collection()
        try:
            # Initialize database
            self.db.init_db()

            # Collect data
            try:
                raw_records = await self.collector.collectBTC(days=days)
            except Exception as e:
                self.error_tracker.record_error('collection', e, {'days': days})
                raise

            # Process data
            try:
                processed_data = self.processor.process_records(raw_records)
            except Exception as e:
                self.error_tracker.record_error('processing', e, {'records': len(raw_records)})
                raise

            # Data Quality Checks
            quality_issues = False
            for currency in settings.SUPPORTED_CURRENCIES:
                currency_data = [r for r in processed_data if r.currency == currency]
                if not currency_data:
                    continue

                prices = [r.price for r in currency_data]
                timestamps = [r.price_timestamp for r in currency_data]
                
                # Run quality checks
                quality_report = self.quality_validator.validate_price_data(
                    prices=prices,
                    timestamps=timestamps
                )

                # Store quality results
                with self.db.get_session() as session:
                    for check in quality_report.checks:
                        result = QualityCheckResult(
                            timestamp=quality_report.timestamp,
                            source=f"btc_price_{currency}",
                            check_name=check.name,
                            passed=check.passed,
                            message=check.message,
                            details=check.details
                        )
                        session.add(result)
                    session.commit()

                # Log quality issues
                if not quality_report.passed:
                    quality_issues = True
                    logger.warning(f"Quality issues found for {currency}: {quality_report.summary}")
                    for check in quality_report.checks:
                        if not check.passed:
                            logger.warning(f"Failed check: {check.message}")
                            self.error_tracker.record_error(
                                'quality',
                                ValueError(check.message),
                                {'currency': currency, 'check': check.name}
                            )
            
            # Validate data before storage
            validation_errors = False
            for currency in settings.SUPPORTED_CURRENCIES:
                currency_data = [r for r in processed_data if r.currency == currency]
                if not currency_data:
                    self.error_tracker.record_error(
                        'validation', 
                        ValueError(f"No data for {currency}"),
                        {'currency': currency}
                    )
                    validation_errors = True  # Set to True when no data
                    continue

                prices = [r.price for r in currency_data]
                timestamps = [r.price_timestamp for r in currency_data]
                validation_result = self.validator.validate_price_data(prices, timestamps)

                if not validation_result.is_valid:
                    validation_errors = True  # Set to True on validation failure
                    self.error_tracker.record_error(
                        'validation',
                        ValueError(validation_result.errors),
                        {'currency': currency}
                    )

            # Stop pipeline if validation failed
            if validation_errors or quality_issues:
                logger.error("Validation or quality checks failed, stopping pipeline")
                raise ValueError("Data validation or quality checks failed")

            # Store data
            with self.db.get_session() as session:
                try:
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

                    logger.info(f"Total records processed: {total_records}")
                    logger.info(f"New records inserted: {inserted_records}")
                    logger.info(f"Duplicate records skipped: {skipped_records}")

                except IntegrityError as e:
                    session.rollback()
                    logger.error(f"Database integrity error: {e}")
                    raise
                except Exception as e:
                    session.rollback()
                    logger.error(f"Database error: {e}")
                    raise

            # Log error summary at the end
            error_summary = self.error_tracker.get_error_summary()
            if error_summary:
                logger.warning(f"Pipeline errors: {error_summary}")
            
            # Record metrics
            self.metrics.end_collection(
                records=len(processed_data),
                retries=self.collector.retries if hasattr(self.collector, 'retries') else 0
            )

            if self.metrics.current_run:
                duration = (self.metrics.current_run.end_time - self.metrics.current_run.start_time).total_seconds()
                logger.info(f"""Collection Metrics:
------------------
Records collected: {self.metrics.current_run.records_collected}
Retries: {self.metrics.current_run.retries}
Duration: {duration:.2f} seconds
Start time: {self.metrics.current_run.start_time}
End time: {self.metrics.current_run.end_time}""")
     
            return processed_data
        except Exception as e:
            self.metrics.end_collection(errors=1)
            self.error_tracker.record_error('pipeline', e)
            logger.error(f"Pipeline error: {e}")
            raise


