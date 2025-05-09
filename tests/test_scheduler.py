# tests/test_scheduler.py
import pytest
import asyncio
from datetime import datetime
from src.utils.scheduler import Scheduler

@pytest.mark.asyncio
async def test_scheduler():
    run_count = 0

    # Create test task
    async def test_task():
        nonlocal run_count
        run_count += 1
        return "Task completed"
    
    # Initialize scheduler
    scheduler = Scheduler()
    scheduler.add_task("test", test_task, interval_minutes=1)

    # Get task
    # task = scheduler.tasks["test"]
    # assert task.name == "test"
    # assert task.interval_minutes == 1
    # assert not task.is_running

    # Run task once
    # await scheduler.run_task(task)
    # assert task.last_run is not None
    try:
        # Run scheduler for a short time
        scheduler_task = asyncio.create_task(scheduler.start())
        # Wait for a short time to let task run
        await asyncio.sleep(2)
        # Stop scheduler
        scheduler.stop()
        await scheduler_task

        # Check if task ran
        assert run_count > 0, "Task didn't run"
    except Exception as e:
        scheduler.stop()
        raise
