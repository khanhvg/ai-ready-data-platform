select
    o.order_id,
    o.customer_id,
    o.store_id,
    o.order_date,
    o.recorded_at,
    o.channel,
    o.status,
    o.payment_method,
    o.promotion_id,
    o.order_total,
    o.is_late_arriving,
    cu.loyalty_tier as customer_loyalty_tier,
    cu.region_id as customer_region_id,
    s.store_name,
    s.store_type,
    s.region_id as store_region_id,
    r.region_name as store_region_name,
    pr.promo_name,
    pr.discount_pct as promo_discount_pct
from {{ ref('stg_orders') }} o
left join {{ ref('stg_customers') }} cu on o.customer_id = cu.customer_id
left join {{ ref('stg_stores') }} s on o.store_id = s.store_id
left join {{ ref('stg_regions') }} r on s.region_id = r.region_id
left join {{ ref('stg_promotions') }} pr on o.promotion_id = pr.promotion_id
