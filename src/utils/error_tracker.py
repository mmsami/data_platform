# src/utils/error_tracker.py
from datetime import datetime
from typing import Dict, List

class ErrorTracker:
    def __init__(self) -> None:
        self.errors: Dict[str, List[str]] = {}
    
    def record_error(self, error_type: str, error: Exception, context: Dict = None):
        if error_type not in self.errors:
            self.errors[error_type] = []
        
        self.errors[error_type].append({
            'timestamp': datetime.now(),
            'error': str(error),
            'context': context or {}
        })

    def get_error_summary(self) -> Dict:
        return {
            error_type: len(errors)
            for error_type, errors in self.errors.items()
        }