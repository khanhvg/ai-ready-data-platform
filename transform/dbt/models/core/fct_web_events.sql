select
    event_id,
    session_id,
    event_type,
    event_ts,
    product_id,
    order_id
from {{ ref('stg_web_events') }}
