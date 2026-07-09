select
    store_id,
    store_name,
    store_type,
    channel,
    region_id,
    city
from {{ source('raw', 'stores') }}
