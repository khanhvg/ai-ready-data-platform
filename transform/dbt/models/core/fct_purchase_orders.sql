select
    po_id,
    supplier_id,
    store_id,
    order_date,
    expected_date,
    status,
    date_diff('day', order_date::date, expected_date::date) as expected_cycle_days
from {{ ref('stg_purchase_orders') }}
