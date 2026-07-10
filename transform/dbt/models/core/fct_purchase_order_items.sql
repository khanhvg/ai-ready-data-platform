select
    po_item_id,
    po_id,
    supplier_id,
    product_id,
    quantity,
    unit_cost,
    line_spend
from {{ ref('int_purchasing') }}
