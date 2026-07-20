-- customer_id is null on purpose for anonymous browsing sessions (~40% rate,
-- see data-generator/schema.md).
select
    session_id,
    customer_id,
    channel,
    device,
    started_at,
    ended_at,
    landing_page
from {{ source('raw', 'web_sessions') }}
