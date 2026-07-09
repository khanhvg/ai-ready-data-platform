-- Product-level sales performance, ranked by revenue. Joins order_items to
-- completed orders only so returns/cancellations don't inflate the ranking.
select
    p.product_id,
    p.sku,
    p.product_name,
    c.category_name,
    sum(oi.quantity) as units_sold,
    round(sum(oi.line_total), 2) as revenue,
    row_number() over (order by sum(oi.line_total) desc) as revenue_rank
from {{ ref('stg_order_items') }} oi
inner join {{ ref('stg_orders') }} o on oi.order_id = o.order_id
inner join {{ ref('stg_products') }} p on oi.product_id = p.product_id
left join {{ ref('stg_product_categories') }} c on p.category_id = c.category_id
where o.status = 'completed'
group by p.product_id, p.sku, p.product_name, c.category_name
order by revenue desc
