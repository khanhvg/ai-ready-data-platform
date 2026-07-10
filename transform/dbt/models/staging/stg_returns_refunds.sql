select
    return_id,
    order_id,
    reason,
    refund_amount,
    return_date
from {{ source('raw', 'returns_refunds') }}
