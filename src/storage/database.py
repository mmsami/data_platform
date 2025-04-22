# src/storage/database.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

class DatabaseManager:
    def __init__(self):
        # Make sure .env is loaded
        load_dotenv()
        
        # Get database URL
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            raise ValueError("DATABASE_URL not found in environment variables")
        
        # Create engine with explicit SSL mode for Neon
        self.engine = create_engine(database_url, connect_args={'sslmode': 'require'})
        self.Session = sessionmaker(bind=self.engine)

    def init_db(self):
        """Initialize the database by creating all tables"""
        Base.metadata.create_all(self.engine)

    def get_session(self):
        """Get a new database session"""
        return self.Session()