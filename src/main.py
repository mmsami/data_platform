# src/main.py
import asyncio
from src.pipelines.btc_pipeline import BTCPipeline
from src.pipelines.news_pipeline import BitcoinNewsPipeline
from src.reports.report_generator import ReportGenerator
from src.analysis.market_analyzer import MarketAnalyzer
from src.storage.database import DatabaseManager
from src.utils.scheduler import Scheduler
from src.utils.logger import logger
import signal

async def run_price_collection():
    """Task for collecting price data"""
    try:
        pipeline = BTCPipeline()
        logger.info("Starting BTC pipeline...")
        results = await pipeline.run(days=1)
        logger.info(f"BTC pipeline complete. Collected {len(results) if results else 0} records")
    except Exception as e:
        logger.error(f"Error in price collection: {e}")
        raise

async def run_news_collection():
    """Task for collecting news"""
    try:
        pipeline = BitcoinNewsPipeline()
        logger.info("Starting news pipeline...")
        await pipeline.run()
        logger.info("News pipeline complete")
    except Exception as e:
        logger.error(f"Error in news collection: {e}")
        raise

async def generate_reports():
    """Task for generating reports"""
    try:
        db = DatabaseManager()
        logger.info("Generating reports...")
        with db.get_session() as session:
            analyzer = MarketAnalyzer(session)
            report_gen = ReportGenerator(analyzer)

            daily_report = report_gen.generate_daily_report()
            weekly_report = report_gen.generate_weekly_report()

            logger.info("Reports generated successfully")
    except Exception as e:
        logger.error(f"Error generating reports: {e}")
        raise

async def print_status(scheduler: Scheduler):
    """Task for printing status reports"""
    status = await scheduler.get_status()
    logger.info("\nTask Status Report:")
    for task_name, task_status in status.items():
        logger.info(f"\nTask: {task_name}")
        logger.info(f"Last Run: {task_status['last_run']}")
        logger.info(f"Success Rate: {task_status['success_rate']*100:.1f}%")
        logger.info(f"Total Runs: {task_status['total_runs']}")
        if task_status['last_error']:
            logger.info(f"Last Error: {task_status['last_error']}")

async def update_dashboard(scheduler: Scheduler):
    """Task for updating dashboard"""
    await scheduler.update_dashboard()

async def main():
    scheduler = None
    try:
        logger.info("Starting data platform...")
        
        # Initialize database
        db = DatabaseManager()
        db.init_db()
        logger.info("Database initialized")

        # Create scheduler
        scheduler = Scheduler()

        # Handle shutdown gracefully
        def signal_handler():
            logger.info("Shutdown signal received")
            if scheduler:
                scheduler.stop()
        
        # Register signal handlers
        for sig in (signal.SIGINT, signal.SIGTERM):
            asyncio.get_event_loop().add_signal_handler(sig, signal_handler)

        # Add tasks with different intervals
        scheduler.add_task("price_collection", run_price_collection, interval_minutes=5)
        scheduler.add_task("news_collection", run_news_collection, interval_minutes=30)
        scheduler.add_task("report_generation", generate_reports, interval_minutes=1440)
        scheduler.add_task("status_report", lambda: print_status(scheduler), interval_minutes=15)
        scheduler.add_task("dashboard_update", lambda: update_dashboard(scheduler), interval_minutes=1)

        logger.info("Starting scheduler. Press Ctrl+C to stop.")
        logger.info(f"Dashboard available at: {scheduler.dashboard_path}")

        # Start scheduler 
        await scheduler.start()
            
    except Exception as e:
        logger.error(f"Error in main: {e}")
        raise
    finally:
        if scheduler:
            scheduler.stop()
        logger.info("Shutdown complete")

if __name__ == "__main__":
    asyncio.run(main())