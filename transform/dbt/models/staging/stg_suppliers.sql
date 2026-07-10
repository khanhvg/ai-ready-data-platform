select
    supplier_id,
    supplier_name,
    region_id,
    lead_time_days,
    reliability_score
from {{ source('raw', 'suppliers') }}
