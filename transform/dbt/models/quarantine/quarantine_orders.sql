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
    is_late_arriving,
    'invalid-order-status' as quality_rule_id,
    case
        when status is null then 'Order status is null or empty after CSV inference.'
        else 'Order status is outside the allowed retail order-status set.'
    end as quality_reason,
    'stg_orders' as source_model
from {{ ref('stg_orders') }}
where
    status is null
    or status not in ('completed', 'cancelled', 'returned', 'pending')
