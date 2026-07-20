-- Current stock position per product/store, plus restock/sale/return/
-- adjustment volume, flagging negative balances for the demo's inventory
-- storytelling.
with latest_position as (
    select
        product_id,
        store_id,
        running_stock_position,
        row_number() over (
            partition by product_id, store_id
            order by movement_date desc, movement_id desc
        ) as rn
    from {{ ref('fct_inventory_movements') }}
),

movement_totals as (
    select
        product_id,
        store_id,
        sum(case when movement_type = 'restock' then quantity else 0 end) as restock_qty,
        sum(case when movement_type = 'sale' then quantity else 0 end) as sale_qty,
        sum(case when movement_type = 'return' then quantity else 0 end) as return_qty,
        sum(case when movement_type = 'adjustment' then quantity else 0 end) as adjustment_qty
    from {{ ref('fct_inventory_movements') }}
    group by product_id, store_id
)

select
    p.product_id,
    p.product_name,
    p.category_name,
    st.store_name,
    st.region_name,
    lp.running_stock_position as current_stock_position,
    mt.restock_qty,
    mt.sale_qty,
    mt.return_qty,
    mt.adjustment_qty,
    lp.running_stock_position < 0 as is_negative_balance
from latest_position lp
inner join movement_totals mt on lp.product_id = mt.product_id and lp.store_id = mt.store_id
inner join {{ ref('dim_products') }} p on lp.product_id = p.product_id
inner join {{ ref('dim_stores') }} st on lp.store_id = st.store_id
where lp.rn = 1
order by current_stock_position asc
