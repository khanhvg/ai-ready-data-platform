select
    po_id,
    supplier_id,
    store_id,
    order_date,
    expected_date,
    status
from {{ source('raw', 'purchase_orders') }}
