# src/utils/task_monitor.py
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional

@dataclass
class TaskStatus:
    name: str
    last_run: Optional[datetime] = None
    last_success: Optional[datetime] = None
    last_error: Optional[str] = None
    success_count: int = 0
    error_count: int = 0
    is_running: bool = False

class TaskMonitor:
    def __init__(self):
        self.task_statuses: Dict[str, TaskStatus] = {}
    
    def register_task(self, task_name: str):
        """Register a new task for monitoring"""
        self.task_statuses[task_name] = TaskStatus(name=task_name)
    
    def update_status(self, task_name: str, success: bool, error: Optional[str] = None):
        """Update task status after execution"""
        status = self.task_statuses.get(task_name)
        if status:
            status.last_run = datetime.now()
            if success:
                status.last_success = datetime.now()
                status.success_count += 1
                status.last_error = None
            else:
                status.error_count += 1
                status.last_error = error
    
    def get_status_report(self) -> Dict:
        """Get status report for all tasks"""
        return {
            name: {
                'last_run': status.last_run,
                'last_success': status.last_success,
                'success_rate': (
                    status.success_count / (status.success_count + status.error_count)
                    if (status.success_count + status.error_count) > 0
                    else 0
                ),
                'total_runs': status.success_count + status.error_count,
                'is_running': status.is_running,
                'last_error': status.last_error
            }
            for name, status in self.task_statuses.items()
        }