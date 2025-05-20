from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys, os
import subprocess
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.pipelines.btc_pipeline import BTCPipeline
from src.pipelines.news_pipeline import BitcoinNewsPipeline
from src.utils.logger import logger

dag = DAG(
    'crypto_data_pipeline',
    default_args={
        'owner': 'airflow',
        'start_date': datetime(2024, 1, 1),
        'retries': 3,
        'retry_delay': timedelta(minutes=5),
    },
    schedule_interval=timedelta(minutes=5),
    catchup=False,
)

def run_main_script(**context):
    subprocess.run(['python', '-m', 'src.main'], check=True)

run_script_task = PythonOperator(
    task_id='run_main_script',
    python_callable=run_main_script,
    dag=dag,
)