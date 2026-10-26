select
    coalesce(job_type, 'Not stated') as job_type,
    count(*) as job_count
from {{ ref('jobs_clean') }}
group by 1
order by job_count desc