-- Daily revenue aggregate, the first customer-facing business mart (P3 demo
-- evidence). Only 'completed' orders count as revenue; other statuses
-- (cancelled/returned/pending/invalid) are excluded but still visible in
-- fct_orders for data-quality demos.
select
    order_date,
    count(*) as completed_order_count,
    sum(order_total) as revenue,
    round(sum(order_total) / count(*), 2) as avg_order_value
from {{ ref('fct_orders') }}
where status = 'completed'
group by order_date
order by order_date
