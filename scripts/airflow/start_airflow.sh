#!/bin/bash
set -e

if [ -f ".env" ]; then
    source .env
fi

export AIRFLOW_HOME="${PWD}/airflow"
export AIRFLOW__CORE__SQL_ALCHEMY_CONN="postgresql+psycopg2://postgres:postgres@localhost:5432/airflow"
export AIRFLOW__CORE__LOAD_EXAMPLES=False

echo "Starting Airflow services..."

# Create Airflow directories if they do not exist
mkdir -p "$AIRFLOW_HOME/dags" "$AIRFLOW_HOME/logs" "$AIRFLOW_HOME/plugins"

# Initialize or upgrade the Airflow metadata database
airflow db migrate

# Start Airflow webserver and scheduler on custom port (8085)
airflow api-server --port 8085
airflow scheduler &

echo "Airflow services started!"
echo "Webserver: http://localhost:8085"
