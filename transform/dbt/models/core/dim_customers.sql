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
from {{ ref('stg_customers') }}
