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

    # Collection settings
    DEFAULT_CURRENCY: str = "eur"
    RATE_LIMIT_CALLS: int = 10
    RATE_LIMIT_PERIOD: int = 60  # in seconds

    @classmethod
    def validate(cls) -> None:
        """Validate required settings."""
        if not cls.DATABASE_URL:
            raise ValueError("DATABASE_URL is required")

# Create a global settings instance
settings = Settings()
# Validate on import
settings.validate()