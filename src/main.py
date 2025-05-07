# src/main.py
import asyncio
from src.pipelines.btc_pipeline import BTCPipeline
from src.pipelines.news_pipeline import BitcoinNewsPipeline
from src.reports.report_generator import ReportGenerator
from src.analysis.market_analyzer import MarketAnalyzer
from src.storage.database import DatabaseManager
from src.utils.logger import logger

async def main():
    try:
        logger.info("Starting data platform...")
        
        # Initialize database
        db = DatabaseManager()
        db.init_db()
        logger.info("Database initialized")

        # Run pipelines
        btc_pipeline = BTCPipeline()
        news_pipeline = BitcoinNewsPipeline()

        # Collect data
        logger.info("Starting BTC pipeline...")
        btc_data = await btc_pipeline.run()
        logger.info(f"BTC pipeline complete. Collected {len(btc_data)} records")
        
        logger.info("Starting news pipeline...")
        news_data = await news_pipeline.run()
        logger.info("News pipeline complete")

        # Generate reports
        logger.info("Generating reports...")
        with db.get_session() as session:
            analyzer = MarketAnalyzer(session)
            report_gen = ReportGenerator(analyzer)
            
            daily_report = report_gen.generate_daily_report()
            logger.info("Daily report generated")
            
            weekly_report = report_gen.generate_weekly_report()
            logger.info("Weekly report generated")
            
        logger.info("All tasks completed successfully")
            
    except Exception as e:
        logger.error(f"Error in main: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())