select
    order_id,
    customer_id,
    store_id,
    order_date,
    recorded_at,
    channel,
    status,
    payment_method,
    promotion_id,
    order_total,
    is_late_arriving
from {{ ref('int_orders_enriched') }}
