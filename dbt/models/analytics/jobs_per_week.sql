select
    date_trunc('week', posted_at)::date as week_start,
    count(*) as job_count
from {{ ref('jobs_clean') }}
where posted_at is not null
group by 1
order by 1