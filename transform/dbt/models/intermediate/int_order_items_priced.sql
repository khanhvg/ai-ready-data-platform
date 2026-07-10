-- product_id may be dangling (controlled orphan-FK scenario, see
-- stg_order_items) -- left join keeps the order-item row visible with null
-- product/category attributes rather than dropping it.
select
    oi.order_item_id,
    oi.order_id,
    oi.product_id,
    p.sku,
    p.product_name,
    p.category_id,
    c.category_name,
    oi.quantity,
    oi.unit_price,
    oi.discount_pct,
    oi.line_total,
    round(oi.quantity * oi.unit_price, 2) as gross_revenue,
    round(oi.quantity * oi.unit_price - oi.line_total, 2) as discount_amount
from {{ ref('stg_order_items') }} oi
left join {{ ref('stg_products') }} p on oi.product_id = p.product_id
left join {{ ref('stg_product_categories') }} c on p.category_id = c.category_id
