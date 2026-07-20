-- Product-level sales performance, ranked by revenue. Joins order items to
-- completed orders only so returns/cancellations don't inflate the ranking.
select
    p.product_id,
    p.sku,
    p.product_name,
    p.category_name,
    sum(oi.quantity) as units_sold,
    round(sum(oi.line_total), 2) as revenue,
    row_number() over (order by sum(oi.line_total) desc) as revenue_rank
from {{ ref('fct_order_items') }} oi
inner join {{ ref('fct_orders') }} o on oi.order_id = o.order_id
inner join {{ ref('dim_products') }} p on oi.product_id = p.product_id
where o.status = 'completed'
group by p.product_id, p.sku, p.product_name, p.category_name
order by revenue desc
