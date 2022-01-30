import os
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from ingest_script import ingest_data

AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")

PG_HOST = os.getenv('PG_HOST')
PG_USER = os.getenv('PG_USER')
PG_PASS = os.getenv('PG_PASS')
PG_PORT = os.getenv('PG_PORT')
PG_DATABASE = os.getenv('PG_DATABASE')

local_workflow = DAG (
    "LocalIngestionDag",
    schedule_interval="0 6 2 * *",
    start_date=datetime(2021, 1, 1)
)

DATETIME_FORMAT = "{{ execution_date.strftime(\'%Y_%m\') }}"
DATASET_FILE = f"yellow_tripdata_{DATETIME_FORMAT}.csv"
DATASET_URL = f"https://s3.amazonaws.com/nyc-tlc/trip+data/{DATASET_FILE}"
OUTPUT_FILE_TEMPLATE = AIRFLOW_HOME + '/output_{{ execution_date.strftime(\'%Y_%m\') }}.csv'
TABLE_NAME_TEMPLATE = f"yellow_taxi_{DATETIME_FORMAT}"


with local_workflow:


    wget_task = BashOperator(
        task_id="wget-file",
        bash_command=f'curl -SL {DATASET_URL} > {OUTPUT_FILE_TEMPLATE}'
    )

    ingestion_task = PythonOperator(
        task_id="ingest",
        python_callable=ingest_data,
        op_kwargs=dict(
            user=PG_USER,
            pwd=PG_PASS,
            host=PG_HOST,
            port=PG_PORT,
            db=PG_DATABASE,
            table_name=TABLE_NAME_TEMPLATE,
            csv_name=OUTPUT_FILE_TEMPLATE
        )
    )

    wget_task >> ingestion_task


    