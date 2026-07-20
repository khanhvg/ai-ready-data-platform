select
    return_id,
    order_id,
    reason,
    refund_amount,
    return_date
from {{ ref('stg_returns_refunds') }}
