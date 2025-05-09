# src/utils/scheduler.py
import asyncio
from datetime import datetime, timedelta
from typing import Callable, Dict, Any
from src.utils.logger import logger
from src.utils.task_monitor import TaskMonitor
from src.utils.dashboard import Dashboard
import os

class Task:
    def __init__(self, name: str, func: Callable, interval_minutes: int):
        self.name = name
        self.func = func
        self.interval_minutes = interval_minutes
        self.last_run: datetime | None = None
        self.is_running = False
    
class Scheduler:
    def __init__(self, dashboard_path: str = "dashboard.html"):
        self.tasks: Dict[str, Task] = {}
        self.running = True
        self.monitor = TaskMonitor()
        self.dashboard_path = dashboard_path
    
    def stop(self):
        """Stop the scheduler"""
        logger.info("Stopping scheduler...")
        self.running = False

    def add_task(self, name: str, func: Callable, interval_minutes: int):
        """Add a task to the scheduler"""
        self.tasks[name] = Task(name, func, interval_minutes)
        self.monitor.register_task(name)
        logger.info(f"Added task: {name} with interval: {interval_minutes} minutes")
        
    async def run_task(self, task: Task):
        """Run a single task"""
        while self.running:
            try:
                now = datetime.now()
                if (not task.last_run or (now - task.last_run).total_seconds() >= task.interval_minutes * 60):
                    logger.info(f"Running task: {task.name}")
                    task.is_running = True
                    await task.func()
                    task.last_run = now
                    task.is_running = False

                    self.monitor.update_status(task.name, success=True)
                    logger.info(f"Completed task: {task.name}")
                
                await asyncio.sleep(60)  # Check every minute
            except Exception as e:
                logger.error(f"Error in task {task.name}: {e}")
                task.is_running = False
                await asyncio.sleep(60)  # Wait before retrying
    
    async def get_status(self) -> Dict:
        """Get current status of all tasks"""
        return self.monitor.get_status_report()
    
    async def update_dashboard(self):
        """Update the dashboard HTML"""
        try:
            status = await self.get_status()
            Dashboard.save_dashboard(status)
        except Exception as e:
            logger.error(f"Error updating dashboard: {e}")

        
    async def start(self):
        """Start the scheduler"""
        logger.info("Starting scheduler")
        tasks = [self.run_task(task) for task in self.tasks.values()]
        await asyncio.gather(*tasks)