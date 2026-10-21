import json
import os
from datetime import date, datetime, timezone

import requests
from dotenv import load_dotenv

load_dotenv()  # reads your key from the .env file

API_KEY = os.getenv("JOOBLE_API_KEY")
URL = f"https://ng.jooble.org/api/{API_KEY}"
KEYWORDS = ["data engineer", "data analyst", "data scientist"]
LOCATION = ""


def fetch_jobs(keyword, page=1):
    payload = {"keywords": keyword, "location": LOCATION, "page": page}
    response = requests.post(URL, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def main():
    if not API_KEY:
        raise SystemExit("Missing JOOBLE_API_KEY. Add it to your .env file.")

    results = []
    for keyword in KEYWORDS:
        data = fetch_jobs(keyword)
        jobs = data.get("jobs", [])
        print(f"{keyword}: {len(jobs)} jobs")
        results.append({
            "keyword": keyword,
            "location": LOCATION,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "response": data,
        })

    filename = f"raw/jooble_{date.today()}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"Saved raw data to {filename}")


def lambda_handler(event, context):
    main()


if __name__ == "__main__":
    main()