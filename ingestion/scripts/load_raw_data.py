import os
import requests
import pandas as pd
from sqlalchemy import create_engine, text

print("Starting raw ingestion...")

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "market_intelligence")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
API_BASE_URL = os.getenv("API_BASE_URL", "http://api_source:5000")

DATABASE_URL = (
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

engine = create_engine(DATABASE_URL)


def ensure_raw_schema():
    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))


def load_external_market_data():
    response = requests.get(f"{API_BASE_URL}/market-data", timeout=30)
    response.raise_for_status()
    df = pd.DataFrame(response.json())
    df.to_sql("raw_market_data", engine, schema="raw", if_exists="replace", index=False)
    print(f"Loaded {len(df)} rows into raw.raw_market_data")


def copy_internal_tables():
    tables = ["customers", "products", "orders"]

    with engine.connect() as conn:
        for table in tables:
            result = conn.execute(text(f"SELECT * FROM {table}"))
            rows = result.fetchall()
            df = pd.DataFrame(rows, columns=result.keys())

            df.to_sql(
                f"raw_{table}",
                engine,
                schema="raw",
                if_exists="replace",
                index=False,
            )
            print(f"Loaded {len(df)} rows into raw.raw_{table}")


ensure_raw_schema()
copy_internal_tables()
load_external_market_data()

print("Raw ingestion completed successfully.")