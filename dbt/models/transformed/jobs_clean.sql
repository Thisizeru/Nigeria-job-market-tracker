with ranked as (
    select
        *,
        row_number() over (
            partition by id
            order by ingested_at desc
        ) as row_num
    from {{ source('raw', 'jooble_jobs') }}
)

select
    id,
    trim(title) as title,
    coalesce(nullif(trim(company), ''), 'Unknown') as company,
    nullif(trim(location), '') as location,
    (location ilike '%remote%') as is_remote,
    nullif(trim(type), '') as job_type,
    nullif(trim(salary), '') as salary,
    source,
    link,
    trim(regexp_replace(
        replace(regexp_replace(snippet, '<[^>]+>', '', 'g'), '&nbsp;', ' '),
        '\s+', ' ', 'g'
    )) as description,
    nullif(left(updated, 19), '')::timestamp as posted_at,
    ingested_at,
    source_file
from ranked
where row_num = 1