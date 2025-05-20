# src/utils/json_encoder.py
import json
from datetime import datetime, timedelta

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, timedelta):
            return str(obj)  # Convert timedelta to string
        return super().default(obj)

def serialize_for_json(obj):
    """Convert datetime and timedelta objects to strings in dictionaries"""
    if isinstance(obj, dict):
        return {k: serialize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [serialize_for_json(x) for x in obj]
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, timedelta):
        return str(obj)  # Convert timedelta to string
    return obj