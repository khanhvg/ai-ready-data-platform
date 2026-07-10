select
    p.product_id,
    p.sku,
    p.product_name,
    p.category_id,
    c.category_name,
    p.unit_price,
    p.is_active
from {{ ref('stg_products') }} p
left join {{ ref('stg_product_categories') }} c on p.category_id = c.category_id
