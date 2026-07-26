select quarantined.order_id
from {{ ref('quarantine_orders') }} as quarantined
inner join {{ ref('ai_ready_customer_product') }} as product
    on product.order_key = 'order_' || substr(
        sha256(cast(quarantined.order_id as varchar) || ':ai-ready-order:v1'),
        1,
        24
    )
