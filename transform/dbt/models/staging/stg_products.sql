select
    product_id,
    sku,
    product_name,
    category_id,
    unit_price,
    is_active
from {{ source('raw', 'products') }}
