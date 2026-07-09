select
    category_id,
    category_name,
    min_price,
    max_price
from {{ source('raw', 'product_categories') }}
