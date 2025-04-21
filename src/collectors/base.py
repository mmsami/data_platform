# src/collectors/base.py
from typing import List, Dict, Any
from datetime import datetime
from dataclasses import dataclass

@dataclass
class DataRecord:
    """Standard format for all collected data"""
    source: str
    data: Dict[str, Any]
    timestamp: datetime

class BaseCollector:
    """Template for all collectors"""
    def __init__(self, name: str) -> None:
        self.name = name
    
    async def collect(self) -> List[DataRecord]:
        """Must be implemented by each collector"""
        raise NotImplementedError