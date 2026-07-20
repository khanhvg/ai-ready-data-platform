select
    payment_id,
    order_id,
    payment_method,
    amount,
    payment_status,
    payment_date
from {{ ref('stg_payments') }}
