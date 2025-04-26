# src/utils/exceptions.py

class DataPlatformError(Exception):
    """Base exception for all platform errors"""
    pass

class ValidationError(DataPlatformError):
    """Raised when data validation fails"""
    pass

class CollectionError(DataPlatformError):
    """Raised when data collection fails"""
    pass