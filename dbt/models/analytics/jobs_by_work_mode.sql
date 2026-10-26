select
    case when is_remote then 'Remote' else 'On-site or unspecified' end as work_mode,
    count(*) as job_count
from {{ ref('jobs_clean') }}
group by 1
order by job_count desc