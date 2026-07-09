select
    movement_id,
    product_id,
    store_id,
    movement_type,
    quantity,
    movement_date
from {{ source('raw', 'inventory_movements') }}
