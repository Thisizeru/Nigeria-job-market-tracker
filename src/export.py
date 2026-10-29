import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

load_dotenv()

TABLES = ["top_skills", "top_companies", "jobs_by_work_mode", "jobs_by_type", "jobs_per_week"]
OUT = Path("dashboard/data")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    engine = create_engine(
        URL.create(
            "postgresql+psycopg2",
            username=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT", "5432")),
            database=os.getenv("DB_NAME"),
        )
    )
    for table in TABLES:
        df = pd.read_sql(f"select * from analytics.{table}", engine)
        df.to_csv(OUT / f"{table}.csv", index=False)
        print(f"{table}: {len(df)} rows")


if __name__ == "__main__":
    main()