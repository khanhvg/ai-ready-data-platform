-- Discounted vs baseline revenue by campaign and channel. Orders with no
-- matching promotion (promotion_id null or expired) are grouped under
-- 'no_promotion' so promo uplift can be read directly against the same
-- channel's baseline average order value.
select
    coalesce(pr.promo_name, 'no_promotion') as promo_name,
    o.channel,
    count(distinct o.order_id) as order_count,
    round(sum(oi.gross_revenue), 2) as gross_revenue,
    round(sum(oi.discount_amount), 2) as total_discount_amount,
    round(sum(oi.line_total), 2) as net_revenue,
    round(sum(oi.line_total) / count(distinct o.order_id), 2) as avg_order_value,
    round(100.0 * sum(oi.discount_amount) / nullif(sum(oi.gross_revenue), 0), 1) as discount_pct_of_gross
from {{ ref('fct_order_items') }} oi
inner join {{ ref('fct_orders') }} o on oi.order_id = o.order_id
left join {{ ref('dim_promotions') }} pr on o.promotion_id = pr.promotion_id
where o.status = 'completed'
group by coalesce(pr.promo_name, 'no_promotion'), o.channel
order by promo_name, o.channel
