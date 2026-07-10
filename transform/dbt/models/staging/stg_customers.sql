-- Duplicate customer_id rows are injected by the generator at a low controlled
-- rate (see data-generator/schema.md). Dedupe here so downstream marts and the
-- `unique` test on customer_id operate on clean data; the raw duplicates are
-- still inspectable directly in raw.customers.
with deduped as (
    select
        *,
        row_number() over (partition by customer_id order by signup_date) as rn
    from {{ source('raw', 'customers') }}
)

select
    customer_id,
    first_name,
    last_name,
    email,
    region_id,
    city,
    loyalty_tier,
    signup_date,
    is_active
from deduped
where rn = 1
