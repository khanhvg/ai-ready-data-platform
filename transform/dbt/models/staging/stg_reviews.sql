select
    review_id,
    product_id,
    customer_id,
    rating,
    review_text,
    review_date
from {{ source('raw', 'reviews') }}
