from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
database_url = os.getenv('DATABASE_URL')
print(f"Connecting to: {database_url}")
engine = create_engine(database_url, connect_args={'sslmode': 'require'})
with engine.connect() as connection:
    print("Connection successful!")