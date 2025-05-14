# src/storage/database.py
from contextlib import contextmanager
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from ..config.settings import settings
from ..utils.logger import logger

class DatabaseManager:
    def __init__(self):
        # Make sure .env is loaded
        # load_dotenv()
        
        # Get database URL
        # database_url = os.getenv('DATABASE_URL')
        if not settings.DATABASE_URL:
            raise ValueError("DATABASE_URL not found in environment variables")
        
        # Create engine with explicit SSL mode for Neon
        self.engine = create_engine(
            settings.DATABASE_URL,
            connect_args={'sslmode': 'require'},
            pool_size=settings.DB_POOL_SIZE,
            max_overflow=settings.DB_MAX_OVERFLOW,
            pool_timeout=settings.DB_POOL_TIMEOUT,
            pool_recycle=settings.DB_POOL_RECYCLE,
            echo=settings.SQL_ECHO
        )
        self.Session = sessionmaker(bind=self.engine)

    def init_db(self):
        """Initialize the database by creating all tables"""
        try:
            Base.metadata.create_all(self.engine)
            logger.info("Database initialization completed")
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise

    @contextmanager
    def get_session(self):
        """Get a database session with automatic cleanup"""
        session = self.Session()
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {e}")
            session.rollback()
            raise
        finally:
            session.close()