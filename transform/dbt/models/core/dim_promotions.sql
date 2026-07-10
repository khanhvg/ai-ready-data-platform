select
    promotion_id,
    promo_name,
    discount_pct,
    start_date,
    end_date,
    channel
from {{ ref('stg_promotions') }}
