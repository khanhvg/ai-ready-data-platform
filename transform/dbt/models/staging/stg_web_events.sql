-- session_id is passed through unclean on purpose: a controlled rate of
-- orphaned FKs (9,000,000+ offset) is injected upstream, flagged at warn
-- severity (see data-generator/schema.md).
select
    event_id,
    session_id,
    event_type,
    event_ts,
    product_id,
    order_id
from {{ source('raw', 'web_events') }}
