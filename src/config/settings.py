# src/config/settings.py
import os
from dotenv import load_dotenv
from typing import Optional

# Load .env once at config level
load_dotenv()

class Settings:
    """Global settings configuration."""

    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    # API settings
    COINGECKO_API_KEY: Optional[str] = os.getenv('COINGECKO_API_KEY')
    COINGECKO_BASE_URL: str = "https://api.coingecko.com/api/v3"
    BINANCE_BASE_URL = "https://api.binance.com/api/v3"
    KRAKEN_BASE_URL = "https://api.kraken.com/0/public"
    RPA_RATE_LIMIT = 10

    # Collection settings
    DEFAULT_CURRENCY: str = "eur"
    SUPPORTED_CURRENCIES: list[str] = ["usd", "eur", "gbp"]
    RATE_LIMIT_CALLS: int = 10
    RATE_LIMIT_PERIOD: int = 60  # in seconds

    # Exchange API credentials
    EXCHANGE1_USERNAME: str = os.getenv("EXCHANGE1_USERNAME")
    EXCHANGE1_PASSWORD: str = os.getenv("EXCHANGE1_PASSWORD")

    # RPA settings
    ENABLE_RPA: bool = os.getenv("ENABLE_RPA", "false").lower() == "true"
    
    # Collection intervals
    PRICE_COLLECTION_INTERVAL: int = int(os.getenv("PRICE_COLLECTION_INTERVAL", "5"))

    # Database settings
    SQL_ECHO: bool = os.getenv('SQL_ECHO', 'false').lower() == 'true'
    DB_POOL_SIZE: int = int(os.getenv('DB_POOL_SIZE', '5'))
    DB_MAX_OVERFLOW: int = int(os.getenv('DB_MAX_OVERFLOW', '10'))
    DB_POOL_TIMEOUT: int = int(os.getenv('DB_POOL_TIMEOUT', '30'))
    DB_POOL_RECYCLE: int = int(os.getenv('DB_POOL_RECYCLE', '1800'))

    # Cache settings
    CACHE_DEFAULT_TTL: int = int(os.getenv('CACHE_DEFAULT_TTL', '300'))
    
    # Batch processing settings
    DEFAULT_BATCH_SIZE: int = int(os.getenv('DEFAULT_BATCH_SIZE', '1000'))
    
    # Performance monitoring
    PERFORMANCE_THRESHOLD: float = float(os.getenv('PERFORMANCE_THRESHOLD', '5.0'))

    @classmethod
    def validate(cls) -> None:
        """Validate required settings."""
        if not cls.DATABASE_URL:
            raise ValueError("DATABASE_URL is required")

# Create a global settings instance
settings = Settings()
# Validate on import
settings.validate()