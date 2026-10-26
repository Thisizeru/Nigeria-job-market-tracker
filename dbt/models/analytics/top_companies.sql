select
    company,
    count(*) as job_count
from {{ ref('jobs_clean') }}
where company <> 'Unknown'
group by company
order by job_count desc
limit 20