-- product_id is passed through unclean on purpose: a controlled rate of
-- dangling FKs (9,000,000+ offset) is injected upstream, flagged at warn
-- severity (see data-generator/schema.md).
select
    po_item_id,
    po_id,
    product_id,
    quantity,
    unit_cost
from {{ source('raw', 'purchase_order_items') }}
