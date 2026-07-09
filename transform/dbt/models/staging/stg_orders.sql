-- Duplicate order_id rows are deduped the same way as stg_customers (see
-- data-generator/schema.md). `status` and `recorded_at` are passed through
-- unclean on purpose: invalid status values and late-arriving records are
-- controlled data-quality scenarios surfaced by the schema tests in
-- _staging__models.yml, not silently cleaned here.
with deduped as (
    select
        *,
        row_number() over (partition by order_id order by recorded_at) as rn
    from {{ source('raw', 'orders') }}
)

select
    order_id,
    customer_id,
    store_id,
    order_date,
    recorded_at,
    channel,
    status,
    payment_method,
    promotion_id,
    order_total,
    recorded_at::date > order_date as is_late_arriving
from deduped
where rn = 1
