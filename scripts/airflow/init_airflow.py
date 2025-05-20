import os
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        os.system('airflow db init')
        os.system(f'airflow users create --username {os.getenv("AIRFLOW_ADMIN_USER")} --firstname Admin --lastname User --role Admin --email admin@example.com --password {os.getenv("AIRFLOW_ADMIN_PASSWORD")}')
        logger.info("Airflow initialization complete")
    except Exception as e:
        logger.error(f"Error during initialization: {e}")
        raise

if __name__ == "__main__":
    main()