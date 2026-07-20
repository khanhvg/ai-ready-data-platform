select
    s.supplier_id,
    s.supplier_name,
    s.region_id,
    r.region_name,
    s.lead_time_days,
    s.reliability_score
from {{ ref('stg_suppliers') }} s
left join {{ ref('stg_regions') }} r on s.region_id = r.region_id
