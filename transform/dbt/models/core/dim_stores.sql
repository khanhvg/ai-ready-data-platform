select
    s.store_id,
    s.store_name,
    s.store_type,
    s.channel,
    s.region_id,
    r.region_name,
    s.city
from {{ ref('stg_stores') }} s
left join {{ ref('stg_regions') }} r on s.region_id = r.region_id
