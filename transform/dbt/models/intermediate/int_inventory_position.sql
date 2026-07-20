-- Source rows carry an unsigned quantity; direction is inferred from
-- movement_type since the raw data has no separate signed-delta column:
-- restock/return add to stock, sale removes from stock. `adjustment` has no
-- direction field in the source system either, so it is treated as an
-- additive correction for this demo (documented assumption, not a defect).
with signed as (
    select
        movement_id,
        product_id,
        store_id,
        movement_type,
        movement_date,
        quantity,
        case
            when movement_type in ('restock', 'return', 'adjustment') then quantity
            when movement_type = 'sale' then -quantity
            else 0
        end as signed_quantity
    from {{ ref('stg_inventory_movements') }}
)

select
    movement_id,
    product_id,
    store_id,
    movement_type,
    movement_date,
    quantity,
    signed_quantity,
    sum(signed_quantity) over (
        partition by product_id, store_id
        order by movement_date, movement_id
    ) as running_stock_position
from signed
