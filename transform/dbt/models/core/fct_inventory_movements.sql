select
    movement_id,
    product_id,
    store_id,
    movement_type,
    movement_date,
    quantity,
    signed_quantity,
    running_stock_position
from {{ ref('int_inventory_position') }}
