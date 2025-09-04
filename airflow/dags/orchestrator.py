import sys
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime, timedelta
from docker.types import Mount

sys.path.append('/opt/airflow/api-request')

from insert_records import connect_to_db, create_table, insert_records
from api_request import fetch_data

def fetch_and_insert():
    data = fetch_data()
    if not isinstance(data, dict):
        raise ValueError(f"API did not return a dict, got: {type(data)}")
    conn = connect_to_db()
    try:
        create_table(conn)
        insert_records(conn, data)
    except Exception as e:
        print(f"An error occurred during execution: {e}")
        raise
    finally:
        if 'conn' in locals():
            conn.close()
            print("Database connection closed.")        

default_args = {
    'description':'Orchestrate data',
    'start_date':datetime(2025, 8, 29),
    'catchup':False,
}

dag = DAG(
    dag_id='weather-api-dbt-orchestrator',
    default_args=default_args,
    schedule=timedelta(minutes=5)
)

with dag:
    task1 = PythonOperator(
        task_id='fetch_and_ingest_data_task',
        python_callable=fetch_and_insert
    )
    task2 = DockerOperator(
        task_id='transform_data_task',
        image='ghcr.io/dbt-labs/dbt-postgres:1.9.latest',
        command='run',
        working_dir='/usr/app',
        mounts=[
            Mount(source='/home/justin/repos/weather-data-project/dbt/my_project',
                target='/usr/app',
                type='bind'),
            Mount(source='/home/justin/repos/weather-data-project/dbt/profiles.yml',
                target='/root/.dbt/profiles.yml',
                type='bind'),
        ],
        network_mode='weather-data-project_my-network',
        docker_url='unix://var/run/docker.sock',
        auto_remove='success'
    )

    task1 >> task2