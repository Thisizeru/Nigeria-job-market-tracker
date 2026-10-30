import json
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import URL

load_dotenv()

engine = create_engine(
    URL.create(
        "postgresql+psycopg2",
        username=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5434")),
        sslmode=os.getenv("DB_SSLMODE", "prefer"),
        database=os.getenv("DB_NAME", "nigeria_jobs"),
    )
)

for file in sorted(Path("raw").glob("jooble_*.json")):
    data = json.loads(file.read_text(encoding="utf-8"))
    pages = data if isinstance(data, list) else [data]
    jobs = [j for p in pages for j in p.get("response", p).get("jobs", [])]

    df = pd.DataFrame(jobs).astype("string")  # keep everything as text, as received
    df["source_file"] = file.name
    df["ingested_at"] = pd.Timestamp.now(tz="UTC")

    with engine.begin() as conn:
        if inspect(conn).has_table("jooble_jobs", schema="raw"):
            conn.execute(
                text("DELETE FROM raw.jooble_jobs WHERE source_file = :f"),
                {"f": file.name},
            )
        df.to_sql("jooble_jobs", conn, schema="raw", if_exists="append", index=False)

    print(f"{file.name}: loaded {len(df)} jobs")