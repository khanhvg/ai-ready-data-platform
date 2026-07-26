select
    'order_' || substr(
        sha256(cast(orders.order_id as varchar) || ':ai-ready-order:v1'),
        1,
        24
    ) as order_key,
    'customer_' || substr(
        sha256(cast(customers.customer_id as varchar) || ':ai-ready-customer:v1'),
        1,
        24
    ) as customer_key,
    case
        when customers.email is null then null
        else 'email_' || substr(
            sha256(lower(customers.email) || ':ai-ready-email:v1'),
            1,
            24
        )
    end as email_pseudonym,
    customers.loyalty_tier,
    customers.is_active,
    orders.order_date,
    orders.channel,
    orders.status as accepted_order_status,
    orders.order_total
from {{ ref('accepted_orders') }} as orders
inner join {{ ref('stg_customers') }} as customers
    on orders.customer_id = customers.customer_id
