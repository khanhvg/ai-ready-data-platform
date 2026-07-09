-- product_id is passed through unclean on purpose: a low controlled rate of
-- dangling FKs (9,000,000+ offset) is injected by the generator to exercise
-- the `relationships` test in _staging__models.yml (see data-generator/schema.md).
select
    order_item_id,
    order_id,
    product_id,
    quantity,
    unit_price,
    discount_pct,
    line_total
from {{ source('raw', 'order_items') }}
