#!/bin/bash
set -e

echo "Stopping Airflow services..."

pkill -f "airflow webserver" || true
pkill -f "airflow scheduler" || true

echo "Airflow services stopped"