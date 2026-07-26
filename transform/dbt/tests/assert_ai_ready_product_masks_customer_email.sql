select product.order_key
from {{ ref('ai_ready_customer_product') }} as product
inner join {{ ref('accepted_orders') }} as accepted
    on product.order_key = 'order_' || substr(
        sha256(cast(accepted.order_id as varchar) || ':ai-ready-order:v1'),
        1,
        24
    )
inner join {{ ref('stg_customers') }} as customer
    on accepted.customer_id = customer.customer_id
where
    product.email_pseudonym is distinct from (
        case
            when customer.email is null then null
            else 'email_' || substr(
                sha256(lower(customer.email) || ':ai-ready-email:v1'),
                1,
                24
            )
        end
    )
    or product.email_pseudonym = customer.email
