select
    order_item_id,
    order_id,
    product_id,
    quantity,
    unit_price,
    discount_pct,
    line_total,
    gross_revenue,
    discount_amount
from {{ ref('int_order_items_priced') }}
