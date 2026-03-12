from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "execution_timeout": timedelta(minutes=30),
}

with DAG(
    dag_id="market_intelligence_360",
    description="Run ingestion, dbt run, and dbt test",
    default_args=default_args,
    start_date=datetime(2026, 3, 1),
    schedule=None,
    catchup=False,
    max_active_runs=1,
    tags=["market-intelligence", "dbt", "postgres"],
) as dag:

    # 1. Task to Ingest Raw Data
    ingest_raw_data = BashOperator(
        task_id="ingest_raw_data",
        bash_command="""
            cd /opt/airflow/project && \
            python ingestion/scripts/load_raw_data.py
        """,
        env={
            "PYTHONPATH": "/opt/airflow/project",
            "POSTGRES_HOST": "warehouse-db",  # Matches service name in docker-compose
            "POSTGRES_PORT": "5432",
            "POSTGRES_DB": "market_intelligence",
            "POSTGRES_USER": "postgres",
            "POSTGRES_PASSWORD": "postgres",
            "API_BASE_URL": "http://api-source:5000", # Matches service name in docker-compose
        },
    )

    # 2. Task to Run dbt transformations
    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="""
            cd /opt/airflow/project/dbt && \
            dbt run --profiles-dir /opt/airflow/.dbt
        """,
        env={
            "DBT_PROFILES_DIR": "/opt/airflow/.dbt",
        },
    )

    # 3. Task to Run dbt tests
    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="""
            cd /opt/airflow/project/dbt && \
            dbt test --profiles-dir /opt/airflow/.dbt
        """,
        env={
            "DBT_PROFILES_DIR": "/opt/airflow/.dbt",
        },
    )

    # Define the Dependency Chain
    ingest_raw_data >> dbt_run >> dbt_test