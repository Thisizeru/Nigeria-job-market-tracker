with skills as (
    select * from (values
        ('SQL', '\ysql\y'),
        ('Python', '\ypython\y'),
        ('Excel', '\yexcel\y'),
        ('Power BI', '\ypower\s*bi\y'),
        ('Tableau', '\ytableau\y'),
        ('AWS', '\yaws\y'),
        ('Azure', '\yazure\y'),
        ('GCP', '\y(gcp|google cloud)\y'),
        ('Spark', '\yspark\y'),
        ('Airflow', '\yairflow\y'),
        ('dbt', '\ydbt\y'),
        ('Docker', '\ydocker\y'),
        ('Kafka', '\ykafka\y'),
        ('Snowflake', '\ysnowflake\y'),
        ('ETL', '\yetl\y'),
        ('Machine Learning', '\ymachine learning\y')
    ) as s(skill, pattern)
),

jobs as (
    select id, lower(title || ' ' || coalesce(description, '')) as text
    from {{ ref('jobs_clean') }}
),

total as (
    select count(*) as total_jobs from jobs
)

select
    s.skill,
    count(*) as job_count,
    round(100.0 * count(*) / max(t.total_jobs), 1) as share_of_jobs_pct
from jobs j
join skills s on j.text ~ s.pattern
cross join total t
group by s.skill
order by job_count desc