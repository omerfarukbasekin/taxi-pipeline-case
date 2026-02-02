from datetime import datetime, timedelta
import sys
import os
import shutil

from airflow import DAG
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.trigger_rule import TriggerRule
from loader.postgres_loader import PostgresTripLoader

sys.path.append("/opt/airflow")

from validation.csv_validator import CSVValidator
from loader.postgres_loader import PostgresTripLoader


INCOMING_PATH = "/data/incoming/output.csv"
OUTPUT_DIR = "/data/history"
REJECTED_DIR = "/data/rejected"


def validate_csv_task():
    validator = CSVValidator(INCOMING_PATH)
    validator.run_all()
    print("CSV validation passed")


def move_csv_success():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.move(INCOMING_PATH, f"{OUTPUT_DIR}/output_{ts}.csv")


def move_csv_failed():
    os.makedirs(REJECTED_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.move(INCOMING_PATH, f"{REJECTED_DIR}/output_{ts}.csv")

def load_csv_to_postgres():
    loader = PostgresTripLoader(
        postgres_conn_id="postgres_trips",
        csv_path=INCOMING_PATH
    )
    loader.run()

with DAG(
    dag_id="Daily_DAG",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    default_args={
        "retries": 1,
        "retry_delay": timedelta(minutes=5)
    }
) as dag:

    wait_for_csv = FileSensor(
        task_id="wait_for_csv",
        filepath=INCOMING_PATH,
        poke_interval=30,
        timeout=300,
        mode="poke"
    )

    validate_task = PythonOperator(
        task_id="validate_csv",
        python_callable=validate_csv_task
    )

    load_task = PythonOperator(
        task_id="load_csv_to_postgres",
        python_callable=load_csv_to_postgres
    )

    success_move = PythonOperator(
        task_id="archive_success",
        python_callable=move_csv_success
    )

    failed_move = PythonOperator(
        task_id="archive_failed",
        python_callable=move_csv_failed,
        trigger_rule=TriggerRule.ONE_FAILED,
        retries=0
    )

    success = EmptyOperator(task_id="success")

    wait_for_csv >> validate_task >> load_task >> success_move >> success
    validate_task >> failed_move
