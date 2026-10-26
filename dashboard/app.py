import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

load_dotenv()  

st.set_page_config(page_title="Nigeria Data Jobs Tracker", layout="wide")


@st.cache_resource
def get_engine():
    url = URL.create(
        "postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "5432")),
        database=os.getenv("DB_NAME"),
    )
    return create_engine(url)


@st.cache_data(ttl=600)
def load(table):
    return pd.read_sql(f"select * from analytics.{table}", get_engine())


skills = load("top_skills")
companies = load("top_companies")
work_mode = load("jobs_by_work_mode")
job_type = load("jobs_by_type")
weekly = load("jobs_per_week")

st.title("Nigeria Data Jobs Tracker")
st.caption("Data job listings collected from Jooble, cleaned with dbt and stored in Postgres.")

total_jobs = int(job_type["job_count"].sum())
remote_jobs = int(work_mode.loc[work_mode["work_mode"] == "Remote", "job_count"].sum())
top_skill = skills.iloc[0]["skill"] if not skills.empty else "n/a"

c1, c2, c3 = st.columns(3)
c1.metric("Jobs tracked", total_jobs)
c2.metric("Remote jobs", remote_jobs)
c3.metric("Most requested skill", top_skill)

left, right = st.columns(2)
with left:
    st.subheader("Most requested skills")
    st.bar_chart(skills.set_index("skill")["job_count"])
    st.caption("Counted from job titles and short descriptions, so real demand is higher.")
with right:
    st.subheader("Top hiring companies")
    st.dataframe(companies, hide_index=True)

left2, right2 = st.columns(2)
with left2:
    st.subheader("Remote vs on-site")
    st.bar_chart(work_mode.set_index("work_mode")["job_count"])
with right2:
    st.subheader("Job types")
    st.bar_chart(job_type.set_index("job_type")["job_count"])

st.subheader("Jobs posted per week")
if weekly.empty:
    st.info("No posting dates available yet.")
else:
    st.line_chart(weekly.set_index("week_start")["job_count"])